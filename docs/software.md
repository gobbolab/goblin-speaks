---
layout: default
title: Software
description: Details on software used to run the Goblin Speaks system.
---

# Software

This page details the software used to run a Goblin Speaks machine.

The software handles the main game loop and also provides terminal based commands for testing the machine which are useful during the build process or when troubleshooting.
It runs as a systemd service in a tmux terminal, allowing the user to operate the Raspberry Pi as normal and optionally tie into the Goblin Speaks terminal session to execute commands.

On launch the software will listen in the background for a coin insertion to start the game.
A series of menu options are available to the operator via the Goblin Speaks terminal.
These can be used to test audio, dispense a card etc.

The github repo with all of the software can be found here: https://github.com/gobbolab/goblin-speaks

## Raspberry PI Setup

The software is designed to run on Raspberry Pi.
A setup script is provided in the main git repository which will handle installation and setup of the software.

It will take the following actions:

- Install system dependencies
- Create a new user named `goblin`
- Create the application directory `home/goblin/goblin-speaks`
- Download the launcher script
- Download the systemd service file
- Configure systemd to start the goblin-speaks program in a tmux session on startup


To run the script, execute this command in your terminal:

```
curl -sL https://raw.githubusercontent.com/gobbolab/goblin-speaks/main/linux/setup.sh | sudo bash
```

## Systemd Service

The setup script will install a goblin-speaks service in systemd that will run automatically when the Raspberry Pi starts up.
This service runs the Goblin Speaks software in a tmux terminal session.

To attach to the terminal session run this command:

```
sudo -u goblin tmux a
```

To view the status of the systemd service, run this command:

```
systemctl status goblin.service
```