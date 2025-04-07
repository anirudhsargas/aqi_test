import subprocess
import os
import sys
import webbrowser
from datetime import datetime

# Configuration
SCRIPTS = {
    'preprocess': 'scripts/preprocess.py',
    'analysis': 'scripts/analysis.py',
    'modeling': 'scripts/modeling.py'
}

REQUIRED_FILES = {
    'input': 'data/dataset.csv',
    'output': 'data/cleaned_dataset.csv'
}

CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
DASHBOARD_URL = "file:///D:/air_quality_project/templates/index.html"

def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_script(script_name):
    script_path = SCRIPTS.get(script_name)
    if not script_path:
        log_message(f"Unknown script: {script_name}", "ERROR")
        return False
    
    if not os.path.exists(script_path):
        log_message(f"Script not found: {script_path}", "ERROR")
        return False

    log_message(f"Starting {script_name}...")
    try:
        result = subprocess.run(
            ["python", script_path],
            check=True,
            capture_output=True,
            text=True
        )
        log_message(f"{script_name} completed successfully\nOutput:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Error in {script_name}:\n{e.stderr}", "ERROR")
        return False
    except Exception as e:
        log_message(f"Unexpected error in {script_name}: {str(e)}", "ERROR")
        return False

def check_files():
    missing_files = [f for f in REQUIRED_FILES.values() if not os.path.exists(f)]
    if missing_files:
        log_message(f"Missing required files: {', '.join(missing_files)}", "ERROR")
        return False
    return True

def open_dashboard():
    try:
        log_message("Opening dashboard in Chrome...")
        webbrowser.get(CHROME_PATH).open(DASHBOARD_URL)
        return True
    except Exception as e:
        log_message(f"Failed to open dashboard: {str(e)}", "ERROR")
        return False

def main():
    log_message("Starting Air Quality Analysis Pipeline")
    
    if not check_files():
        sys.exit(1)
    
    success = all([
        run_script('preprocess'),
        run_script('analysis'),
        run_script('modeling')
    ])
    
    if success:
        log_message("All tasks completed successfully!")
        open_dashboard()
    else:
        log_message("Pipeline failed - check error messages above", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()