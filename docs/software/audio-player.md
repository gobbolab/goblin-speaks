---
layout: default
title: Audio Player
description: Details on how the Goblin Speaks Audio Player works.
---

# Audio Player

The [`AudioPlayer`](https://github.com/gobbolab/goblin-speaks/blob/main/src/audio/audio_player.py) class handles all sound playback for the machine. It uses `pygame.mixer` for low-latency audio playback and organizes sounds into user-defined **sound banks**.

## Sound Banks

Sound banks are defined in `config.yml` under `audio_player.sound_banks`. You can create as many banks as you need — there are no predetermined categories. Each bank maps to a subdirectory under the sounds root directory.

```yaml
audio_player:
  sounds_dir: ~/.goblin-speaks/sounds   # optional, this is the default
  sound_banks:
    activation:
      mode: random
    pre_show:
      mode: sequential
    show:
      mode: sequential
    post_show:
      mode: sequential
```

With the config above, the audio player will load sounds from:

- `~/.goblin-speaks/sounds/activation/`
- `~/.goblin-speaks/sounds/pre_show/`
- `~/.goblin-speaks/sounds/show/`
- `~/.goblin-speaks/sounds/post_show/`

### Sounds Directory

The `sounds_dir` key sets the root directory where sound bank subdirectories are located. It defaults to `~/.goblin-speaks/sounds`. Tilde (`~`) is expanded automatically.

### Supported Formats

On startup, each bank's directory is scanned for `.mp3` and `.wav` files. Files are loaded in alphabetical order, which determines their sequential playback order.

If a bank's directory does not exist, it is created automatically and the bank is initialized with no sounds. This ensures the expected directory structure is always in place, ready for sound files to be added.

## Playback Modes

Each sound bank has an independent playback mode which is used when a specific filename is not provided for play:

- **`sequential`** *(default)*: Plays the next sound in sequential order, cycling back to the first after the last. This ensures every sound gets equal play.
- **`random`**: A sound is chosen at random each time.

## Playing Sounds

Sound playback is controlled through the `audio` component in your [sequence](configuration.md#sequence). The built-in `audio` component is always available — you don't need to declare it in `components`.

### By Bank (Next Sound)

The `play` action selects the next sound from a bank based on its playback mode.

```yaml
- component: audio
  action: play
  args:
    bank_name: show
```

### By Filename

You can play a specific sound by name. The `file_name` can be the full filename (e.g. `greeting.wav`) or just the stem (e.g. `greeting`).

```yaml
- component: audio
  action: play
  args:
    bank_name: activation
    file_name: greeting
```

### Sound Sequences

The `play_sequence` action plays one sound from each of the specified banks in order.
This is useful for chaining sounds from different banks together to make full phrases or effects.

```yaml
- component: audio
  action: play_sequence
  args:
    sound_types: [pre_show, show, post_show]
```

Unknown bank names in the sequence are skipped with a warning. Banks with no loaded sounds are also skipped silently.

### Blocking Playback

Both `play` and `play_sequence` are **non-blocking by default** — they return immediately while audio plays in the background. Set `block: true` to wait for playback to finish before returning.

```yaml
- component: audio
  action: play
  args:
    bank_name: activation
    block: true

- component: audio
  action: play_sequence
  args:
    sound_types: [pre_show, show, post_show]
    block: true
```

### Capturing Duration

Both actions return the total duration of the played audio in seconds. Use `output` to capture this value for later steps — for example, to run an animation for exactly as long as the audio plays:

```yaml
- component: audio
  action: play_sequence
  args:
    sound_types: [pre_show, show, post_show]
  output: duration
- component: goblin_body
  action: animate
  args:
    duration: $duration
```

## Configuration Reference

All keys are optional. The defaults shown below are used if a key is absent.

```yaml
audio_player:
  # Root directory for sound bank subdirectories
  sounds_dir: ~/.goblin-speaks/sounds

  # Each key under sound_banks defines a bank
  # Directory is always sounds_dir/bank_name
  sound_banks:
    my_bank:
      mode: sequential    # sequential | random
```
