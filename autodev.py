import os
import json
import subprocess
import requests
from datetime import datetime
from prompt_toolkit import prompt
import speech_recognition as sr  # For voice commands

# Load config
CONFIG_PATH = os.path.expanduser("~/.autodev/config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]

# Local knowledge base
KNOWLEDGE_PATH = "knowledge.json"

def auto_fix(error):
    """Fix errors using local knowledge or OpenRouter"""
    # Check local knowledge base
    with open(KNOWLEDGE_PATH, "r") as f:
        kb = json.load(f)
        for key in kb:
            if key in error.lower():
                return kb[key]
    
    # Use OpenRouter if not found locally
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"Fix this error locally: {error}"}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def install(tool):
    """Install tools using OS-specific scripts"""
    os_type = subprocess.check_output("uname", shell=True).decode().strip().lower()
    
    # Termux detection
    if "termux" in os.environ.get("PREFIX", ""):
        os_type = "termux"
    
    script = f"install_scripts/{os_type}.sh"
    
    if not os.path.exists(script):
        print(f"AutoDev: Unsupported OS: {os_type}")
        return
    
    print(f"AutoDev: Installing {tool}...")
    subprocess.run(f"bash {script} {tool}", shell=True)

def generate(template):
    """Generate IaC templates"""
    if template == "docker":
        subprocess.run(f"cp templates/Dockerfile .", shell=True)
    elif template == "k8s":
        subprocess.run(f"cp templates/kubernetes.yml .", shell=True)
    else:
        print("Template not found")

def scan():
    """Run security scans"""
    print("Running Python security scan...")
    subprocess.run("bandit -r .", shell=True)
    print("Running Node.js security scan...")
    subprocess.run("npm audit", shell=True)

def monitor():
    """Show system resources"""
    import psutil
    print(f"CPU: {psutil.cpu_percent()}% | Memory: {psutil.virtual_memory().percent}%")

def listen():
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_sphinx(audio)  # Offline mode
    except sr.UnknownValueError:
        return ""

def main():
    print("AutoDev Assistant Ready 🤖")
    print("Commands: install <tool>, fix <error>, generate <template>, scan, monitor, voice")
    
    while True:
        user_input = prompt(">> ")
        
        # Voice command activation
        if user_input == "voice":
            print("Say a command (e.g., 'Install Docker')...")
            voice_command = listen().lower()
            print(f"Recognized: {voice_command}")
            
            if "install" in voice_command:
                tool = voice_command.split()[-1]
                install(tool)
            
            elif "generate" in voice_command:
                template = voice_command.split()[-1]
                generate(template)
            
            elif "fix" in voice_command:
                error = " ".join(voice_command.split()[1:])
                print(auto_fix(error))
            
            elif "scan" in voice_command:
                scan()
            
            elif "monitor" in voice_command:
                monitor()
            
            else:
                print(f"Executing: {voice_command}")
                subprocess.run(voice_command, shell=True)
        
        # Text command handlers
        elif user_input.startswith("install "):
            tool = user_input.split(" ", 1)[1]
            install(tool)
        
        elif user_input.startswith("fix "):
            error = user_input.split(" ", 1)[1]
            print(auto_fix(error))
        
        elif user_input.startswith("generate "):
            template = user_input.split(" ", 1)[1]
            generate(template)
        
        elif user_input == "scan":
            scan()
        
        elif user_input == "monitor":
            monitor()
        
        else:
            # Execute shell commands
            result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print("🚨 Error Detected! Run 'fix' to get help.")

if __name__ == "__main__":
    main()
