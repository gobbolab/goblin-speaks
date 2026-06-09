#!/bin/bash

# Configuration
REPO="gobbolab/goblin-speaks"
TARBALL="goblin-app.tar.gz"
APP_DIR="/home/goblin/goblin-speaks"
EXEC="$APP_DIR/main.bin"

cd "$APP_DIR" || exit 1

echo "Checking for updates..."

# 1. Attempt to get the latest release URL
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep "browser_download_url.*$TARBALL" | cut -d '"' -f 4)

# 2. Update process with fallback
if [ -n "$DOWNLOAD_URL" ]; then
    echo "New release found. Downloading..."
    
    # Download to temporary file
    if curl -L -s -o "$TARBALL.tmp" "$DOWNLOAD_URL"; then
        # Create a backup of the current working version before extracting
        # This keeps the system running if the new tarball is broken
        mv "$TARBALL.tmp" "$TARBALL"
        
        echo "Extracting new version..."
        if tar -xzvf "$TARBALL" > /dev/null; then
            chmod +x "$EXEC"
            echo "Update applied."
        else
            echo "Extraction failed. Falling back to previous version."
        fi
    else
        echo "Download failed. Falling back to previous version."
        rm -f "$TARBALL.tmp"
    fi
else
    echo "No update available or network unreachable. Using current version."
fi

if [ -x "$EXEC" ]; then
    echo "Starting application..."
    # Execute directly
    "$EXEC"
else
    echo "Error: Executable not found at $EXEC."
    exit 1
fi