---
layout: default
title: Goblin Speaks Example
description: How the Goblin Speaks fortune teller machine is configured using the framework.
---

# Goblin Speaks Example

The Goblin Speaks fortune teller is the first machine built on the framework, and the one it takes its name from. It pairs a [Goblin Speaks Body](components/goblin-speaks-animatronic-body.md) and [Head](components/goblin-speaks-head.md) with a [Card Dispenser](components/goblin-speaks-card-dispenser.md): the head speaks a fortune while the body animates, then the dispenser hands the player a card to take home.

<iframe width="560" height="315" src="https://youtube.com/embed/22QMtMoQO5U?si=L_L5Q7h8ckz2mF6Z" title="Goblin Speaks" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Configuration

The machine is driven by this configuration file, which consists of three main sections:

- `audio_player` — configures the sound banks used by the machine.
- `components` — defines the machine's physical components and what software they run.
- `sequences` — defines the named sequences the machine can run.

```yaml
audio_player:
  sound_banks:
    pre_fortune:
      mode: random
    fortune:
      mode: sequential
    post_fortune:
      mode: random
    activation:
      mode: random

components:
  goblin_body:
    type: animatronic
    class: gs_body
  card_dispenser:
    type: dispenser
    class: single_stepper
    dispense_steps: 2048
    step_delay: 0.0015

sequences:
  fortune:
    - component: audio
      action: play_sequence
      args:
        sound_types: [pre_fortune, fortune, post_fortune]
      output: duration
    - component: goblin_body
      action: animate
      args:
        duration: $duration
    - component: card_dispenser
      action: dispense
```

### Sound Banks

The [Audio Player](software/audio-player.md) is set up with four sound banks, each holding a different kind of sound:

- `activation` — a sound played when the machine is activated
- `pre_fortune` — a general intro voice line, played in `random` order so it varies between activations.
- `fortune` — the fortune voice line itself, played in `sequential` order so every fortune gets told before any repeat.
- `post_fortune` — a line asking the player to play again, played in `random` order so it varies between activations.

These sound banks are used later in the `fortune` sequence to allow the machine to combine random pre_fortune and post_fortune lines with a sequentially selected fortune.

### Components

Two components are declared:

- `goblin_body` — a [Goblin Speaks Body](components/goblin-speaks-animatronic-body.md), using the `gs_body` animatronic class.
- `card_dispenser` — a [Goblin Speaks Card Dispenser](components/goblin-speaks-card-dispenser.md), using the `single_stepper` dispenser class. `dispense_steps` and `step_delay` tune how far and how fast the stepper motor turns to push out a single card.

See the [Configuration](software/configuration.md) page for the full set of component types and fields.

### Sequence

The `fortune` sequence runs through three steps:

1. `audio.play_sequence` plays one sound from each of `pre_fortune`, `fortune`, and `post_fortune` in order, and captures the total playback duration as `$duration`.
2. `goblin_body.animate` runs the body's animation routine for `$duration`, so the goblin's mouth and arm move for exactly as long as it's speaking.
3. `card_dispenser.dispense` pushes out a single fortune card once the show finishes.
