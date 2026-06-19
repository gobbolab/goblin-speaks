#!/bin/bash

# Configuration
REPO="gobbolab/goblin-speaks"
DATA_DIR="/home/goblin/goblin-speaks"
EXEC="/opt/goblin-speaks/goblin-speaks"

cd "$DATA_DIR" || exit 1

echo "Checking for updates..."

# 1. Attempt to get the latest .deb release URL (including prereleases)
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases" | grep "browser_download_url.*\.deb" | head -n 1 | cut -d '"' -f 4)

# 2. Update process with fallback
if [ -n "$DOWNLOAD_URL" ]; then
    echo "New release found. Downloading..."
    
    DEB_FILE="$DATA_DIR/goblin-speaks-update.deb"
    
    if curl -L -s -o "$DEB_FILE" "$DOWNLOAD_URL"; then
        echo "Installing update via apt..."
        if apt install -y "$DEB_FILE"; then
            rm -f "$DEB_FILE"
            echo "Update applied."
        else
            echo "Installation failed. Falling back to current version."
            rm -f "$DEB_FILE"
        fi
    else
        echo "Download failed. Falling back to current version."
        rm -f "$DEB_FILE"
    fi
else
    echo "No update available or network unreachable. Using current version."
fi

if [ -x "$EXEC" ]; then
    echo "Starting application..."
    exec "$EXEC" run "$@"
else
    echo "Error: Executable not found at $EXEC."
    exit 1
fi