import os
import time
import datetime
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

# Try to import pyautogui, but handle the case where it's not available
try:
    import pyautogui
    HAS_DISPLAY = True
except:
    print("Warning: pyautogui not available - screenshot functionality disabled")
    HAS_DISPLAY = False

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Configuration
SCREENSHOTS_DIR = "../screenshots"
METADATA_FILE = "../metadata.json"
GROQ_API_KEY = "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" 
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Ensure directories exist
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Initialize metadata file if it doesn't exist
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        json.dump([], f)

def load_metadata():
    try:
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('../frontend/css', path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('../frontend/js', path)

@app.route('/capture', methods=['POST'])
def capture_screenshot():
    try:
        data = request.get_json()
        name = data.get('name', f"Screenshot_{int(time.time())}")
        
        if not HAS_DISPLAY:
            # In headless mode, we'll create a dummy entry with a timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            
            # Create a placeholder image file for development
            with open(filepath, "w") as f:
                f.write("Placeholder for screenshot")
            
            # Update metadata
            metadata = load_metadata()
            metadata.append({
                "id": len(metadata) + 1,
                "name": name,
                "filename": filename,
                "timestamp": timestamp,
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "path": filepath
            })
            save_metadata(metadata)
            
            return jsonify({"success": True, "message": "Development mode: Screenshot placeholder created", "filename": filename})
        else:
            # Normal mode with display available
            screenshot = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            screenshot.save(filepath)
            
            metadata = load_metadata()
            metadata.append({
                "id": len(metadata) + 1,
                "name": name,
                "filename": filename,
                "timestamp": timestamp,
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "path": filepath
            })
            save_metadata(metadata)
            
            return jsonify({"success": True, "message": "Screenshot captured successfully", "filename": filename})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/screenshots', methods=['GET'])
def get_screenshots():
    metadata = load_metadata()
    return jsonify(metadata)

@app.route('/screenshots/<filename>', methods=['GET'])
def get_screenshot(filename):
    return send_from_directory(SCREENSHOTS_DIR, filename)

@app.route('/query', methods=['POST'])
def query_screenshots():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"success": False, "error": "No query provided"}), 400
            
        metadata = load_metadata()
        
        # Prepare screenshot data for Groq
        screenshots_info = []
        for item in metadata:
            screenshots_info.append({
                "name": item["name"],
                "datetime": item["datetime"],
                "filename": item["filename"]
            })
            
        # Prepare prompt for Groq
        prompt = f"""
        I have these screenshots with timestamps:
        {json.dumps(screenshots_info, indent=2)}
        
        The user query is: "{query}"
        
        Based on the timestamps and names, which screenshots would be relevant to this query?
        Please return a JSON object with:
        1. An explanation of what the user was doing
        2. A list of relevant screenshot filenames
        """
        
        # Call Groq API
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 500
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return jsonify({"success": False, "error": f"Groq API error: {response.text}"}), 500
            
        # Process Groq response
        groq_response = response.json()
        ai_response = groq_response["choices"][0]["message"]["content"]
        
        # Extract JSON from AI response
        try:
            # Try to directly parse the response
            result = json.loads(ai_response)
        except:
            # If that fails, try to find JSON within text
            import re
            json_match = re.search(r'```json\n(.*?)\n```', ai_response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                # Create a simple response
                result = {
                    "explanation": "I found some potentially relevant screenshots based on your query.",
                    "screenshots": [item["filename"] for item in metadata[:3]]  # Return top 3 as fallback
                }
        
        return jsonify({"success": True, "result": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)