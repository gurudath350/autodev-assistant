
#!/bin/bash
echo "AutoDev Setup"
echo "Enter OpenRouter API Key:"
read -s API_KEY
echo "Preferred model (e.g., 'gpt-3.5-turbo'):"
read MODEL

# Create config directory
mkdir -p ~/.autodev
echo "{\"api_key\": \"$API_KEY\", \"model\": \"$MODEL\"}" > ~/.autodev/config.json

# Install dependencies
pip install -r requirements.txt

# Create systemd service
echo "[Unit]
Description=AutoDev Backend
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/autodev_api.py
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/autodev.service

sudo systemctl daemon-reload
sudo systemctl enable autodev
sudo systemctl start autodev

echo "AutoDev is running in the background! Use 'journalctl -u autodev' for logs."
