# goblin-speaks
Code for the bartop sized goblin fortune teller machine

## Raspberry PI Setup

### Add Goblin User

```
sudo adduser goblin
sudo usermod -aG goblin
sudo usermod -aG video,audio,gpio,i2c,spi,dialout goblin
```

### Add App Directory

As the goblin user

```
cd ~
mkdir goblin-speaks
```

Save the `launcher.sh` file inside the newly created directory.

Make `launcher.sh` executable.

```
sudo chmod +x launcher.sh
```

### Install tmux

```
sudo apt-get update
sudo apt-get install tmux
```

### Setup Systemd Service

```
sudo nano /etc/systemd/system/goblin.service
```

Paste the goblin.service file contents into this file.

Then enable the service:

```
sudo systemctl daemon-reload
sudo systemctl enable goblin.service
sudo systemctl start goblin.service
```

### Attaching to tmux

`tmux attach -t goblin`