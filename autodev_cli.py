import requests
import json

API_URL = "http://localhost:5000"

def install(tool):
    response = requests.post(f"{API_URL}/install/{tool}")
    print(response.json())

def fix(error):
    response = requests.post(f"{API_URL}/fix", json={"error": error})
    print(response.json())

def generate(template):
    response = requests.post(f"{API_URL}/generate/{template}")
    print(response.json())

def voice():
    response = requests.post(f"{API_URL}/voice")
    print(response.json())

if __name__ == "__main__":
    import sys
    command = sys.argv[1]
    if command == "install":
        install(sys.argv[2])
    elif command == "fix":
        fix(sys.argv[2])
    elif command == "generate":
        generate(sys.argv[2])
    elif command == "voice":
        voice()
