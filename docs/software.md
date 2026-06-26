---
layout: default
title: Software
description: Details on software used to run the Goblin Speaks Fortune Teller Framework.
---

# Software

## Overview

The Goblin Speaks software is a Python-based application designed to run on Raspberry Pi. It orchestrates various aspects of the fortune teller machine including:

- **Play orchestration**: Manages the sequence of events (audio, animation, dispensing) via the [`Player`](https://github.com/gobbolab/goblin-speaks/tree/main/src/player) module. The `DefaultPlayer` handles selecting a random audio file, triggering the animatronic for the duration of the audio, and then dispensing a card.
- **Animatronics control**: Manages servo motors for mouth and arm animations via the [`GSBody`](https://github.com/gobbolab/goblin-speaks/blob/main/src/animatronic/gs_body.py) class
- **Card dispensing**: Controls the stepper motor-driven card dispenser via the [`GSCardDispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/gs_card.py) class
- **Audio playback**: Handles random audio selection and playback via the [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio_player.py) class
- **Command-line interface**: Provides CLI commands for machine operation and testing

The software is built using the `typer` framework, which provides a clean command-line interface. Under the default setup, it runs as a systemd service in a tmux terminal session, allowing the Raspberry Pi to continue operating normally while the Goblin Speaks application runs in the background.

The framework is designed to be highly moddable. Each core component (Animatronics, Dispensers, Players) is defined by an abstract interface. You can create your own custom components (like dispenser for a different type of prize) by simply implementing the required interface and plugging it into the framework. This allows for endless customization of the fortune teller's physical hardware and software flow.

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

## Configuration

A wide range of settings are available to configure a Goblin Speaks machine.
These values are held in a yaml file located in `/opt/goblin-speaks/config.yml`
Using the config file is entirely optional as all values have fallback defaults.
Details on the available config values and their defaults can be found in the docs for each configurable component of the framework.

## Audio Player

The [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio_player.py) class handles all sound playback for the machine. It uses `pygame.mixer` for low-latency audio playback and manages four independent sound banks, each with its own directory and playback mode.

Sound banks are selected using the `SoundType` enum, which is the single entry point for all playback:

```python
audio_player.play(SoundType.SHOW)
```

### Sound Categories

| `SoundType` | Purpose | Default Directory |
|---|---|---|
| `ACTIVATION` | Played when the machine is triggered/activated | `/opt/goblin-speaks/sounds/activation` |
| `PRE_SHOW` | Played before the main fortune-telling sequence begins. ("Come close while Goblin tells your fortune.") | `/opt/goblin-speaks/sounds/pre_show` |
| `SHOW` | Played during the main fortune-telling sequence. ("Goblin sees great treasure in your future!") | `/opt/goblin-speaks/sounds/show` |
| `POST_SHOW` | Played after the main sequence completes. ("How about giving Goblin more money for more fortunes?") | `/opt/goblin-speaks/sounds/post_show` |

On startup, the audio player scans each directory for `.mp3` files and loads them into memory. The number of sounds found in each category is printed to the logs.

### Playback Modes

Each sound category independently supports two playback modes:

- **`sequential`** *(default)*: Sounds are played in order, cycling back to the first after the last one plays. This ensures every sound gets equal airtime.
- **`random`**: A sound is chosen at random each time. Useful for more unpredictable variation.

### Configuration

The audio player is configured via `config.yml`. All keys are optional — the defaults shown below are used if a key is absent.

```yaml
audio_player:
  pre_show_sound_dir: /opt/goblin-speaks/sounds/pre_show
  pre_show_sound_mode: sequential       # sequential | random
  show_sound_dir: /opt/goblin-speaks/sounds/show
  show_sound_mode: sequential           # sequential | random
  post_show_sound_dir: /opt/goblin-speaks/sounds/post_show
  post_show_sound_mode: sequential      # sequential | random
  activation_sound_dir: /opt/goblin-speaks/sounds/activation
  activation_sound_mode: sequential     # sequential | random
```

### Adding Audio Files

Place `.mp3` files in the appropriate directory:

- **Pre-show sounds**: `/opt/goblin-speaks/sounds/pre_show/`
- **Show sounds**: `/opt/goblin-speaks/sounds/show/`
- **Post-show sounds**: `/opt/goblin-speaks/sounds/post_show/`
- **Activation sounds**: `/opt/goblin-speaks/sounds/activation/`

All four directories are created automatically during package installation. Restart the service after adding new files for them to be loaded:

```bash
sudo systemctl restart goblin.service
```

## Contributing

The framework is designed to be modular and moddable, allowing you to design and integrate your own components.
Pull requests are welcome for new component types or improvements to existing ones.
There are currently two types of components in the framework:

**Hardware Components**: These represent physical hardware devices connected to the machine.

   - Animatronics (Animated armatures for characters and creatures in the machine)
   - Dispensers (Used to dispense fortune cards or other objects)

**Software Components**: These manage the logic and flow of the machine entirely in software.

   - Players (Orchestrators that combine audio, animatronics, and dispensers to execute the fortune telling sequence)

### Adding a New Animatronic Implementation

To add a new animatronic type:

1. Create a new class that extends the `Animatronic` base class
2. Implement the `animate(duration)` and `test()` methods
3. Register it in the `AnimatronicFactory` in `src/animatronic/factory.py`
4. Update your `goblin-speaks-config.yml` to specify the new type

### Adding a New Dispenser Implementation

To add a new dispenser type:

1. Create a new class that extends the `Dispenser` base class
2. Implement the `dispense()` and `test()` methods
3. Register it in the `DispenserFactory` in `src/dispenser/factory.py`
4. Update your `goblin-speaks-config.yml` to specify the new type

This modular architecture makes it easy to experiment with different hardware configurations and implementations.