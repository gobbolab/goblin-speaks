#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e 

# 0. Root Check
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this setup script as root (use sudo)."
  exit 1
fi

# Configuration Variables
USERNAME="goblin"
APP_DIR="/home/$USERNAME/goblin-speaks"
RAW_URL="https://raw.githubusercontent.com/gobbolab/goblin-speaks/main"

echo "=== Starting Goblin Speaks Setup ==="

# 1. Install system dependencies (tmux)
echo "[+] Checking for required packages..."
if ! command -v tmux &> /dev/null; then
    echo "[+] Installing tmux..."
    apt-get update
    apt-get install -y tmux
    echo "[✓] tmux installed."
else
    echo "[✓] tmux is already installed."
fi

# 2. Create the user idempotently
if id "$USERNAME" &>/dev/null; then
    echo "[✓] User '$USERNAME' already exists."
else
    echo "[+] Creating user '$USERNAME'..."
    useradd -m -s /bin/bash "$USERNAME"
fi

# 3. Create the application directory
echo "[+] Ensuring application directory exists..."
mkdir -p "$APP_DIR"

# 4. Download the launcher script
echo "[+] Downloading launcher.sh..."
# The -f flag ensures curl fails cleanly if a 404 error occurs
if curl -sL -f "$RAW_URL/linux/launcher.sh" -o "$APP_DIR/launcher.sh"; then
    chmod +x "$APP_DIR/launcher.sh"
    echo "[✓] launcher.sh downloaded and made executable."
else
    echo "[!] Error: Could not download launcher.sh. Check the URL."
    exit 1
fi

# 5. Download the systemd service file
echo "[+] Downloading goblin.service..."
if curl -sL -f "$RAW_URL/linux/goblin.service" -o /etc/systemd/system/goblin.service; then
    echo "[✓] goblin.service downloaded."
else
    echo "[!] Error: Could not download goblin.service."
    echo "    Make sure the service file is pushed to your GitHub repository."
    exit 1
fi

# 6. Set strict ownership
# This ensures the goblin user has full control over its directory
echo "[+] Setting ownership to $USERNAME:$USERNAME..."
chown -R "$USERNAME:$USERNAME" "$APP_DIR"

# 7. Configure systemd (Idempotent by nature)
echo "[+] Reloading systemd daemon..."
systemctl daemon-reload

echo "[+] Enabling goblin.service to start on boot..."
systemctl enable goblin.service

echo "[+] Restarting goblin.service to apply changes..."
systemctl restart goblin.service

echo "=== Setup Complete! ==="
echo "Check the live application status with: systemctl status goblin.service"
echo "Attach to the application terminal with: tmux attach -t goblin"