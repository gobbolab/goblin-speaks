---
layout: default
title: Software Overview
description: Details on software used to run the Goblin Speaks Penny Arcade Framework.
---

# Software

## Overview

The Goblin Speaks software is a config-driven Python framework for building penny arcade style machines on Raspberry Pi. A single YAML file defines the machine's physical components — animatronics, dispensers, audio — and its play sequence, so you can change what your machine does without writing any code.

The framework is built around abstract interfaces for each component type, making it highly moddable. Create custom components by implementing an interface, registering it with the factory, and referencing it in your config. It runs as a systemd service via `tmux` and provides a `typer`-based CLI for operation and testing.

## Raspberry Pi Setup

The software is designed to run on Raspberry Pi. A setup script is provided in the `linux/` directory which automates the installation and configuration process.

[Read more about Raspberry Pi Setup](raspberry-pi-setup.md)

## CLI

The software provides a command-line interface built with `typer`. It includes commands for running the machine, testing individual components through an interactive menu, updating to the latest release, and generating plugin skeleton files.

[Read more about the CLI](cli.md)

## Configuration

The machine is configured through a YAML file located at `/etc/goblin-speaks/config.yml`. The config file has two main sections:

This config-driven approach means you can completely change your machine's behavior — add new components, reorder the play sequence etc. by editing this file.

[Read more about Configuration](configuration.md)

## Audio Player

The `AudioPlayer` class handles all sound playback for the machine. It uses `pygame.mixer` for low-latency audio playback and manages four independent sound banks, each with its own directory and playback mode.

[Read more about the Audio Player](audio-player.md)

## Plugins

The framework supports plugins, allowing you to create and use your own custom components without modifying the core codebase. Drop a Python file into the plugins directory and reference it in your config — no need to touch the framework source.

[Read more about Plugins](plugins.md)