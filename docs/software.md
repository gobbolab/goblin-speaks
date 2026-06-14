---
layout: default
title: Software
description: Details on software used to run the Goblin Speaks Fortune Teller Framework.
---

# Software

## Overview

The Goblin Speaks software is a Python-based application designed to run on Raspberry Pi. It orchestrates various aspects of the fortune teller machine including:

- **Animatronics control**: Manages servo motors for mouth and arm animations via the [`GSBody`](https://github.com/gobbolab/goblin-speaks/blob/main/src/animatronic/gs_body.py) class
- **Card dispensing**: Controls the stepper motor-driven card dispenser via the [`GSCardDispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/gs_card.py) class
- **Audio playback**: Handles random audio selection and playback via the [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio_player.py) class
- **Command-line interface**: Provides CLI commands for machine operation and testing

The software is built using the `typer` framework, which provides a clean command-line interface. Under the default setup, runs as a systemd service in a tmux terminal session, allowing the Raspberry Pi to continue operating normally while the Goblin Speaks application runs in the background.

## Raspberry Pi Setup

The software is designed to run on Raspberry Pi. A setup script is provided in the `linux/` directory which automates the installation and configuration process.

### Running the Setup Script

Execute this command on your Raspberry Pi:

```bash
curl -sL https://raw.githubusercontent.com/gobbolab/goblin-speaks/main/linux/setup.sh | sudo bash
```

### What the Setup Script Does

The [`setup.sh`](https://github.com/gobbolab/goblin-speaks/blob/main/linux/setup.sh) script performs the following actions:

1. **Installs system dependencies**: Installs `tmux` which is required for running the application in a persistent session
2. **Creates a dedicated user**: Creates a `goblin` user account that will run the application
3. **Creates application directory**: Sets up `/home/goblin/goblin-speaks` as the application home directory
4. **Downloads launcher script**: Retrieves [`launcher.sh`](https://github.com/gobbolab/goblin-speaks/blob/main/linux/launcher.sh) which handles automatic updates and application startup
5. **Creates global command**: Links the application to `/usr/local/bin/goblin-speaks` making it available system-wide
6. **Installs systemd service**: Downloads and configures [`goblin.service`](https://github.com/gobbolab/goblin-speaks/blob/main/linux/goblin.service) to start the application on boot
7. **Sets permissions**: Ensures the `goblin` user has full ownership of the application directory

### The Launcher Script

The [`launcher.sh`](https://github.com/gobbolab/goblin-speaks/blob/main/linux/launcher.sh) script is executed by the systemd service on startup. It performs the following:

1. **Checks for updates**: Queries the GitHub API for the latest release of the Goblin Speaks application
2. **Downloads new versions**: If an update is available, downloads and extracts the compiled application binary
3. **Maintains backups**: Keeps a backup of the previous version in case the new release fails to extract properly
4. **Starts the application**: Executes the compiled Goblin Speaks binary with the `run` command

This approach ensures the machine can automatically receive updates while maintaining stability through backup versioning.

### The Systemd Service

The [`goblin.service`](https://github.com/gobbolab/goblin-speaks/blob/main/linux/goblin.service) file configures systemd to:

- Start the application automatically when the Raspberry Pi boots
- Run the application as the `goblin` user in a tmux session named `goblin`
- Properly clean up the tmux session when the service stops

## Using the Application

Once the setup script completes, the Goblin Speaks application is available as a command-line tool.

### Available Commands

The application provides the following CLI commands:

#### `goblin-speaks run`
Starts the application in normal operation mode.
This is the command used when the application is started by the systemd service.
The application will:
- Load all audio files from the current directory
- Listen for the configured activation methods
- Execute the play sequence when activated

#### `goblin-speaks test`
Opens an interactive test menu with the following options:

- **1. Play**: Executes a full play sequence (audio + animation + dispensing)
- **2. Test Animatronic**: Runs a test animation on the configured animatronic
- **3. Test Card**: Dispenses an object from the configured dispenser
- **4. Test Audio**: Plays a random audio file from the loaded audio files
- **0. Exit**: Exits the application

### Accessing the Application Terminal

By default, the application runs in a tmux session. To attach to the session and interact with it:

```bash
sudo -u goblin tmux a
```

To detach from the session without stopping it, press `Ctrl+B` followed by `D`.

### Checking Service Status

To view the current status of the Goblin Speaks systemd service:

```bash
systemctl status goblin.service
```

To view service logs:

```bash
sudo journalctl -u goblin.service -f
```

The `-f` flag will follow the logs in real-time.

### Restarting the Service

If you need to restart the application:

```bash
sudo systemctl restart goblin.service
```

## Audio Files

The application loads MP3 audio files from its working directory. When the application starts, it will scan for all `.mp3` files and display them in the logs. These audio files are selected randomly during play.

Place your fortune teller audio files in `/home/goblin/goblin-speaks/` for the application to discover them automatically.