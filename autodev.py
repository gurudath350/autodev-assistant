import os
import json
import subprocess
import requests
from prompt_toolkit import prompt

# Load config
CONFIG_PATH = os.path.expanduser("~/.autodev/config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]

def auto_fix(error):
    """Use OpenRouter to analyze errors."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"Error: {error}\n\nFix this with step-by-step commands."}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def install(tool):
    """OS-agnostic tool installation."""
    os_type = subprocess.check_output("uname", shell=True).decode().strip().lower()
    script = f"install_scripts/{os_type}.sh"
    # In the install() function:
os_type = subprocess.check_output("uname", shell=True).decode().strip().lower()

# Add Termux detection
if "termux" in os.environ.get("PREFIX", ""):
    os_type = "termux"
    
    if not os.path.exists(script):
        print(f"AutoDev: Unsupported OS: {os_type}")
        return
    
    print(f"AutoDev: Installing {tool}...")
    subprocess.run(f"bash {script} {tool}", shell=True)

def main():
    print("AutoDev Assistant Ready 🤖")
    print("Commands: install <tool>, fix <error>, or type any shell command")
    
    while True:
        user_input = prompt(">> ")
        
        if user_input.startswith("install "):
            tool = user_input.split(" ", 1)[1]
            install(tool)
        
        elif user_input.startswith("fix "):
            error = user_input.split(" ", 1)[1]
            print(auto_fix(error))
        
        else:
            # Execute shell commands and auto-detect errors
            result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print("🚨 Error Detected! Run 'fix' to get help.")
