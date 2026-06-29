---
layout: default
title: Software Overview
description: Details on software used to run the Goblin Speaks Fortune Teller Framework.
---

# Software

## Overview

The Goblin Speaks software is a Python-based application designed to run on Raspberry Pi. It uses a fully config-driven architecture where the machine's physical components and its play sequence are both defined in a single YAML configuration file. This means you can change what your machine does — and in what order — without writing any code.

The software orchestrates various aspects of the fortune teller machine including:

- **Animatronics control**: Manages animatronic routines via the [`Animatronic`](https://github.com/gobbolab/goblin-speaks/blob/main/src/animatronic/base.py) interface
- **Dispensing**: Controls item or prize dispensers via the [`Dispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/base.py) interface
- **Audio playback**: Handles audio selection and playback via the [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio_player.py) class
- **Command-line interface**: Provides CLI commands for machine operation and testing

The software is built using the `typer` framework, which provides a clean command-line interface. Under the default setup, it runs as a systemd service in a tmux terminal session, allowing the Raspberry Pi to continue operating normally while the Goblin Speaks application runs in the background.

The framework is designed to be highly moddable. Each core component type (Animatronics, Dispensers, Activators) is defined by an abstract interface. You can create your own custom components (like a dispenser for a different type of prize) by implementing the required interface, registering it with the appropriate factory, and adding it to your config file. This allows for endless customization of the fortune teller's physical hardware and behavior without modifying the core framework.

## Raspberry Pi Setup

The software is designed to run on Raspberry Pi. A setup script is provided in the `linux/` directory which automates the installation and configuration process.

[Read more about Raspberry Pi Setup](raspberry-pi-setup.md)

## Configuration

The machine is configured through a YAML file located at `/etc/goblin-speaks/config.yml`. The config file has two main sections:

This config-driven approach means you can completely change your machine's behavior — add new components, reorder the play sequence etc. by editing this file.

[Read more about Configuration](configuration.md)

## Audio Player

The `AudioPlayer` class handles all sound playback for the machine. It uses `pygame.mixer` for low-latency audio playback and manages four independent sound banks, each with its own directory and playback mode.

[Read more about the Audio Player](audio-player.md)

## Contributing

The framework is designed to be modular and moddable, allowing you to design and integrate your own components.
Pull requests are welcome for new component types or improvements to existing ones.

[Read more about Contributing](contributing.md)