
#!/bin/bash
echo "AutoDev Setup"
echo "Enter OpenRouter API Key (free tier available at openrouter.ai):"
read -s API_KEY
echo "Preferred model (e.g., 'gpt-3.5-turbo'):"
read MODEL

# Create config directory
mkdir -p ~/.autodev
echo "{\"api_key\": \"$API_KEY\", \"model\": \"$MODEL\"}" > ~/.autodev/config.json

echo "Setup complete! Install dependencies with 'pip install -r requirements.txt'"
