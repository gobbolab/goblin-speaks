---
layout: default
title: Software Overview
description: Details on software used to run the Goblin Speaks Fortune Teller Framework.
---

# Software

## Overview

The Goblin Speaks software is a Python-based application designed to run on Raspberry Pi. It orchestrates various aspects of the fortune teller machine including:

- **Play orchestration**: Manages the sequence of events (audio, animation, dispensing) via the [`Player`](https://github.com/gobbolab/goblin-speaks/tree/main/src/player) module. The `DefaultPlayer` handles selecting a random audio file, triggering the animatronic for the duration of the audio, and then dispensing a card.
- **Animatronics control**: Manages animatronic routines via the [`Animatronic`](https://github.com/gobbolab/goblin-speaks/blob/main/src/animatronic/base.py) interface
- **Dispensing**: Controls item or prize dispensers via the [`Dispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/base.py) interface
- **Audio playback**: Handles audio selection and playback via the [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio_player.py) class
- **Command-line interface**: Provides CLI commands for machine operation and testing

The software is built using the `typer` framework, which provides a clean command-line interface. Under the default setup, it runs as a systemd service in a tmux terminal session, allowing the Raspberry Pi to continue operating normally while the Goblin Speaks application runs in the background.

The framework is designed to be highly moddable. Each core component (Animatronics, Dispensers, Players) is defined by an abstract interface. You can create your own custom components (like dispenser for a different type of prize) by simply implementing the required interface and plugging it into the framework. This allows for endless customization of the fortune teller's physical hardware and software flow.

## Raspberry Pi Setup

The software is designed to run on Raspberry Pi. A setup script is provided in the `linux/` directory which automates the installation and configuration process.

[Read more about Raspberry Pi Setup](software/raspberry-pi-setup.md)

## Configuration

A wide range of settings are available to configure a Goblin Speaks machine.
These values are held in a yaml file located in `/opt/goblin-speaks/config.yml`
Using the config file is entirely optional as all values have fallback defaults.
Details on the available config values and their defaults can be found in the docs for each configurable component of the framework.

## Audio Player

The `AudioPlayer` class handles all sound playback for the machine. It uses `pygame.mixer` for low-latency audio playback and manages four independent sound banks, each with its own directory and playback mode.

[Read more about the Audio Player](software/audio-player.md)

## Contributing

The framework is designed to be modular and moddable, allowing you to design and integrate your own components.
Pull requests are welcome for new component types or improvements to existing ones.

[Read more about Contributing](software/contributing.md)