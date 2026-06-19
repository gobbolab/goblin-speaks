#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e 

# 0. Root Check
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this setup script as root (use sudo)."
  exit 1
fi

REPO="gobbolab/goblin-speaks"

echo "=== Starting Goblin Speaks Setup ==="

# 1. Fetch the latest .deb download URL (including prereleases)
echo "[+] Fetching latest release from GitHub..."
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases" | grep "browser_download_url.*\.deb" | head -n 1 | cut -d '"' -f 4)

if [ -z "$DOWNLOAD_URL" ]; then
    echo "[!] Error: Could not find a release to download. Check https://github.com/$REPO/releases"
    exit 1
fi

echo "[+] Downloading: $DOWNLOAD_URL"
DEB_FILE="/tmp/goblin-speaks.deb"
curl -L -s -o "$DEB_FILE" "$DOWNLOAD_URL"
echo "[✓] Download complete."

# 2. Install the .deb — apt resolves dependencies (e.g. tmux) and postinst handles user/systemd setup
echo "[+] Installing package..."
apt install -y "$DEB_FILE"
rm -f "$DEB_FILE"

echo "=== Setup Complete! ==="
echo "Check the live application status with: systemctl status goblin.service"
echo "Attach to the application terminal with: sudo -u goblin tmux a"