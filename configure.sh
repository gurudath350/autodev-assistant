#!/bin/bash
echo "AutoDev Setup"
echo "Enter OpenRouter API Key:"
read -s API_KEY
echo "Preferred model (e.g., 'gpt-4'):"
read MODEL

# Save config
mkdir -p ~/.autodev
echo "{\"api_key\": \"$API_KEY\", \"model\": \"$MODEL\"}" > ~/.autodev/config.json

echo "AutoDev configured! Run 'python3 autodev.py' to start."
