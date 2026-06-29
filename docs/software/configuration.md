---
layout: default
title: Configuration
description: How to configure components and play sequences for a Goblin Speaks machine.
---

# Configuration

The Goblin Speaks machine is configured through a single YAML file located at `/etc/goblin-speaks/config.yml`. The config file defines which components are attached to your machine and the sequence of actions that run each time the machine is activated.

## Components

The `components` section declares every hardware and software component attached to your machine. Each component is given a name (your choice) and configured with a `type`, `class`, and any component-specific settings.

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
| `activator` | Triggers that start the play sequence (buttons, sensors, etc.) | `gpiozero_button` |

### Component Names

The name you give a component (e.g. `goblin_body`, `card_dispenser`) is how you reference it in the `sequence` section. Choose descriptive names that make sense for your build.

### Built-in Components

The `audio` component is always available and does not need to be declared in the `components` section. It provides access to the [Audio Player](audio-player.md) and its sound banks.

## Sequence

The `sequence` section defines the ordered list of steps that the `SequencePlayer` executes each time the machine is activated. Steps run in order from top to bottom.

```yaml
sequence:
  - component: audio
    action: play_sequence
    args:
      sound_types: [pre_show, show, post_show]
    output: duration
  - component: goblin_body
    action: animate
    args:
      duration: $duration
  - component: card_dispenser
    action: dispense
```

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

Each component type exposes different actions you can call from the sequence:

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

Below is a complete configuration file that sets up a machine with an animatronic body, a card dispenser, and a play sequence that plays audio, animates the body for the duration of the audio, then dispenses a card:

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

sequence:
  - component: audio
    action: play_sequence
    args:
      sound_types: [pre_show, show, post_show]
    output: duration
  - component: goblin_body
    action: animate
    args:
      duration: $duration
  - component: card_dispenser
    action: dispense
```
