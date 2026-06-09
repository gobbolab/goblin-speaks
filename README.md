# goblin-speaks
Code for the bartop sized goblin fortune teller machine

## Raspberry PI Setup

The setup.sh script will install the goblin speaks softare on a Raspberry Pi.

It will take the following actions:
- Install system dependencies
- Create a new user named `goblin`
- Create the application directory `home/goblin/goblin-speaks`
- Download the launcher script
- Download the systemd service file
- Configure systemd to start the goblin-speaks program in a tmux session on startup

```
curl -sL https://raw.githubusercontent.com/gobbolab/goblin-speaks/main/linux/setup.sh | sudo bash
```