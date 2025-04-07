from flask import Flask, request, jsonify, render_template
import subprocess
import os
import pandas as pd
from werkzeug.utils import secure_filename

class Config:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if not (file and allowed_file(file.filename)):
        return jsonify({"error": "Only CSV files allowed"}), 400
    
    try:
        filename = secure_filename('dataset.csv')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "path": filepath}), 200
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

SCRIPTS = [
    "scripts/preprocess.py",
    "scripts/analysis.py",
    "scripts/modeling.py"
]

@app.route('/api/run_analysis', methods=['POST'])
def run_analysis():
    results = []
    for script in SCRIPTS:
        try:
            if not os.path.exists(script):
                return jsonify({"error": f"Script not found: {script}"}), 404
                
            result = subprocess.run(
                ["python", script],
                check=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            results.append({
                "script": script,
                "success": True,
                "output": result.stdout
            })
        except subprocess.CalledProcessError as e:
            return jsonify({
                "error": f"Analysis failed at {script}",
                "details": e.stderr,
                "completed_steps": results
            }), 500
        except subprocess.TimeoutExpired:
            return jsonify({
                "error": f"Timeout expired for {script}",
                "completed_steps": results
            }), 500
    
    return jsonify({
        "message": "Analysis completed successfully",
        "steps": results
    }), 200

@app.route('/api/chart_data')
def get_chart_data():
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'cleaned_dataset.csv')
        if not os.path.exists(filepath):
            return jsonify({"error": "No analysis data available"}), 404
            
        df = pd.read_csv(filepath)
        required_columns = {'Date', 'PM2.5'}
        
        if not required_columns.issubset(df.columns):
            return jsonify({"error": f"Required columns not found. Available: {list(df.columns)}"}), 400
            
        return jsonify({
            "dates": df['Date'].tolist(),
            "pm25": df['PM2.5'].tolist(),
            "columns": list(df.columns)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)