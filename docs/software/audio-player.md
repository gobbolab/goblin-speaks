---
layout: default
title: Audio Player
description: Details on how the Goblin Speaks Audio Player works.
---

# Audio Player

The [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio_player.py) class handles all sound playback for the machine. It uses `pygame.mixer` for low-latency audio playback and manages four independent sound banks, each with its own directory and playback mode.

Sound banks are selected using the `SoundType` enum, which is the single entry point for all playback:

```python
audio_player.play(SoundType.SHOW)
```

## Sound Categories

| `SoundType` | Purpose | Default Directory |
|---|---|---|
| `ACTIVATION` | Played when the machine is triggered/activated | `/opt/goblin-speaks/sounds/activation` |
| `PRE_SHOW` | Played before the main fortune-telling sequence begins. ("Come close while Goblin tells your fortune.") | `/opt/goblin-speaks/sounds/pre_show` |
| `SHOW` | Played during the main fortune-telling sequence. ("Goblin sees great treasure in your future!") | `/opt/goblin-speaks/sounds/show` |
| `POST_SHOW` | Played after the main sequence completes. ("How about giving Goblin more money for more fortunes?") | `/opt/goblin-speaks/sounds/post_show` |

On startup, the audio player scans each directory for `.mp3` files and loads them into memory. The number of sounds found in each category is printed to the logs.

## Playback Modes

Each sound category independently supports two playback modes:

- **`sequential`** *(default)*: Sounds are played in order, cycling back to the first after the last one plays. This ensures every sound gets equal airtime.
- **`random`**: A sound is chosen at random each time. Useful for more unpredictable variation.

## Configuration

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

## Adding Audio Files

Place `.mp3` files in the appropriate directory:

- **Pre-show sounds**: `/opt/goblin-speaks/sounds/pre_show/`
- **Show sounds**: `/opt/goblin-speaks/sounds/show/`
- **Post-show sounds**: `/opt/goblin-speaks/sounds/post_show/`
- **Activation sounds**: `/opt/goblin-speaks/sounds/activation/`

All four directories are created automatically during package installation. Restart the service after adding new files for them to be loaded:

```bash
sudo systemctl restart goblin.service
```
