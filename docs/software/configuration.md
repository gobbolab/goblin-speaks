---
layout: default
title: Configuration
description: How to configure components and play sequences for a Goblin Speaks machine.
---

# Configuration

The Goblin Speaks machine is configured through a single YAML file located at `/etc/goblin-speaks/config.yml`. The config file wires together an audio player, hardware components, activators that trigger sequences, and the sequences themselves.

## Audio Player

The `audio` component is always available and does not need to be declared anywhere in the config. It provides access to the [Audio Player](audio-player.md) and its sound banks, and can be referenced directly from any sequence step as `component: audio`.

See [Audio Player](audio-player.md) for details on configuring sound banks and files.

## Activators

Activators are components that watch for a trigger condition — a button press, a sensor signal, a coin drop — and fire a named sequence when that condition is met. They are declared in the `activators` section. Each activator is given a name (your choice), a `type`, the `sequence` it should play when triggered, and any type-specific settings.

```yaml
activators:
  push_button:
    type: gpiozero_button
    sequence: fortune
    trigger_pin: 21
```

### Activator Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | The activator implementation to use. |
| `sequence` | Yes | The name of a sequence (defined in `sequences`) to play when this activator fires. |
| *(other keys)* | No | Type-specific settings passed through to the implementation. |

### Activator Types

#### `gpiozero_button`

A GPIO button or digital sensor backed by the [gpiozero](https://gpiozero.readthedocs.io/) library. Compatible with physical buttons, IR beam sensors, reed switches, and any other component that signals via a digital GPIO pin.

| Setting | Default | Description |
|---------|---------|-------------|
| `trigger_pin` | `21` | The GPIO pin number to listen on. |

## Components

The `components` section declares every hardware component attached to your machine other than activators. Each component is given a name (your choice) and configured with a `type`, `class`, and any component-specific settings.

```yaml
components:
  goblin_body:
    type: animatronic
    class: gs_body
  card_dispenser:
    type: dispenser
    class: single_stepper
    dispense_steps: 2048
    step_delay: 0.0015
```

### Component Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | The component category. Determines which factory creates it. |
| `class` | Yes | The specific implementation class to instantiate. |
| *(other keys)* | No | Component-specific settings passed through to the implementation. |

### Component Types

| Type | Description | Available Classes |
|------|-------------|-------------------|
| `animatronic` | Controls animatronic movement and routines | `gs_body` |
| `dispenser` | Controls item/prize dispensing mechanisms | `single_stepper` |

### Component Names

The name you give a component (e.g. `goblin_body`, `card_dispenser`) is how you reference it in the `sequences` section. Choose descriptive names that make sense for your build.

## Sequences

The `sequences` section defines named sequences of steps that the machine can execute. Each key under `sequences` is a sequence name you choose, mapped to an ordered list of steps. Steps within a sequence run in order from top to bottom.

```yaml
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

Defining multiple named sequences lets a single machine support more than one routine — for example a full `fortune` sequence and a shorter `greeting` sequence — which can be wired up to different [activators](#activators). The [test menu](cli.md#menu) lists every sequence defined in `sequences` so you can run each one individually.

### Step Fields

| Field | Required | Description |
|-------|----------|-------------|
| `component` | Yes | The name of a component declared in `components` (or the built-in `audio` component). |
| `action` | Yes | The method to call on the component. |
| `args` | No | A map of keyword arguments to pass to the action method. |
| `output` | No | A variable name to capture the action's return value for use by later steps. |

### Variable References

Steps can pass data to later steps using the `output` field and `$variable` references. When a step declares `output: duration`, its return value is stored under the name `duration`. Later steps can reference it with `$duration` in their `args`.

In the example above:

1. The `audio.play_sequence` step returns the total duration of the queued sounds and stores it as `$duration`.
2. The `goblin_body.animate` step receives `$duration` as its `duration` argument, so the animatronic runs for exactly as long as the audio plays.

Variable references work inside lists as well. A reference to an output that hasn't been produced yet will raise an error at runtime.

### Available Actions

Each component type exposes different actions you can call from a sequence:

**Audio** (`audio`)

| Action | Args | Returns | Description |
|--------|------|---------|-------------|
| `play` | `bank_name`, `file_name` (optional), `block` (optional) | `float` (duration) | Play a sound from a sound bank. If `file_name` is given, plays that specific file; otherwise plays the next sound. If `block` is `true`, waits for the sound to finish. |
| `play_sequence` | `sound_types` (list), `block` (optional) | `float` (total duration) | Queue and play sounds from multiple banks in order. If `block` is `true`, waits for all sounds to finish. |

**Animatronic**

| Action | Args | Returns | Description |
|--------|------|---------|-------------|
| `animate` | `duration` (float) | — | Run the animation routine for the specified duration in seconds. |

**Dispenser**

| Action | Args | Returns | Description |
|--------|------|---------|-------------|
| `dispense` | `count` (int, optional) | — | Dispense one or more items. Defaults to 1. |

## Full Example

Below is a complete configuration file that sets up a machine with an animatronic body, a card dispenser, a GPIO button that triggers the `fortune` sequence, and the sequences themselves:

```yaml
components:
  goblin_body:
    type: animatronic
    class: gs_body
  card_dispenser:
    type: dispenser
    class: single_stepper
    dispense_steps: 2048
    step_delay: 0.0015

activators:
  fortune_button:
    type: gpiozero_button
    sequence: fortune
    trigger_pin: 21

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
