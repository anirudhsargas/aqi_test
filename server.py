from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Configuration
class Config:
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

app.config.from_object(Config)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(secure_filename(filename))
    return f"{base}_{timestamp}{ext}"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            "error": "File type not allowed",
            "allowed_types": list(app.config['ALLOWED_EXTENSIONS'])
        }), 400
    
    try:
        unique_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        file.save(file_path)
        
        file_stats = os.stat(file_path)
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_path": file_path,
            "file_name": unique_filename,
            "file_size": file_stats.st_size,
            "upload_time": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "File upload failed",
            "details": str(e)
        }), 500

@app.route('/list_files', methods=['GET'])
def list_uploaded_files():
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(path):
                files.append({
                    "name": filename,
                    "size": os.path.getsize(path),
                    "modified": os.path.getmtime(path)
                })
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)