#!/bin/bash

# Configuration
REPO="gobbolab/goblin-speaks"
TARBALL="goblin-app.tar.gz"
APP_DIR="/home/goblin/goblin-speaks"
EXEC="./main"

cd "$APP_DIR" || exit 1

echo "Checking for updates..."

# 1. Attempt to get the download URL
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep "browser_download_url.*$TARBALL" | cut -d '"' -f 4)

# 2. Only attempt download if URL is found
if [ -n "$DOWNLOAD_URL" ]; then
    echo "New release found. Downloading..."
    
    # Download to a temporary file first
    if curl -L -s -o "$TARBALL.tmp" "$DOWNLOAD_URL"; then
        # If download succeeded, overwrite the old tarball
        mv "$TARBALL.tmp" "$TARBALL"
        # Extract the new release
        tar -xzvf "$TARBALL" > /dev/null
        chmod +x "$EXEC"
        echo "Update applied successfully."
    else
        echo "Download failed. Cleaning up..."
        rm -f "$TARBALL.tmp"
    fi
else
    echo "No new release or cannot reach GitHub. Proceeding with current version."
fi

# 3. Fallback logic: check if executable exists, even if the update failed
if [ -x "$EXEC" ]; then
    echo "Starting application..."
    "$EXEC"
else
    echo "Error: No executable found to run. Exiting."
    exit 1
fi