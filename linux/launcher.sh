#!/bin/bash

# Configuration
REPO="gobbolab/goblin-speaks"
BIN_NAME="main-arm64.bin"
APP_DIR="/home/pi/goblin-speaks"

# Ensure we are in the correct directory
cd "$APP_DIR" || exit 1

echo "Checking for latest release from $REPO..."

# Use GitHub API to find the download URL for the latest main-arm64.bin
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep "browser_download_url.*$BIN_NAME" | cut -d '"' -f 4)

if [ -n "$DOWNLOAD_URL" ]; then
    echo "Found new version. Downloading from $DOWNLOAD_URL..."
    
    # Download to a temporary file first so we don't break the existing one if internet drops
    if curl -L -s -o "$BIN_NAME.new" "$DOWNLOAD_URL"; then
        mv "$BIN_NAME.new" "$BIN_NAME"
        chmod +x "$BIN_NAME"
        echo "Update complete."
    else
        echo "Download failed. Falling back to existing binary."
        rm -f "$BIN_NAME.new"
    fi
else
    echo "Could not reach GitHub or find release. Falling back to existing binary."
fi

# Execute the application
if [ -x "./$BIN_NAME" ]; then
    echo "Starting $BIN_NAME..."
    ./$BIN_NAME
else
    echo "Error: $BIN_NAME not found or not executable. Exiting."
    exit 1
fi
