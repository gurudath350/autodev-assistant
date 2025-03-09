from flask import Flask, request, jsonify
import subprocess
import json
import os
import requests
from speech_recognition import Recognizer, Microphone

app = Flask(__name__)

# Load config
CONFIG_PATH = os.path.expanduser("~/.autodev/config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]

# Local knowledge base
KNOWLEDGE_PATH = "knowledge.json"

def auto_fix(error):
    """Fix errors via local knowledge or OpenRouter"""
    with open(KNOWLEDGE_PATH, "r") as f:
        kb = json.load(f)
        for key in kb:
            if key in error.lower():
                return {"command": kb[key]}
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"Fix this error: {error}"}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return {"command": response.json()["choices"][0]["message"]["content"]}

@app.route("/install/<tool>", methods=["POST"])
def install(tool):
    """Install tools via API"""
    script = "install_scripts/debian.sh"
    subprocess.run(f"bash {script} {tool}", shell=True)
    return jsonify({"status": "success", "tool": tool})

@app.route("/fix", methods=["POST"])
def fix():
    """Fix errors via API"""
    error = request.json["error"]
    return jsonify(auto_fix(error))

@app.route("/generate/<template>", methods=["POST"])
def generate(template):
    """Generate IaC templates"""
    if template == "docker":
        subprocess.run("cp templates/Dockerfile .", shell=True)
    elif template == "k8s":
        subprocess.run("cp templates/kubernetes.yml .", shell=True)
    return jsonify({"status": "success", "template": template})

@app.route("/voice", methods=["POST"])
def voice_command():
    """Handle voice commands"""
    recognizer = Recognizer()
    with Microphone() as source:
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_sphinx(audio)
        return jsonify({"command": command})
    except:
        return jsonify({"error": "Voice recognition failed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
