---
layout: default
title: GSCardDispenser Class
description: Details on the software implementation of the Goblin Speaks Card Dispenser.
---

# `GSCardDispenser` Class

The [`GSCardDispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/gs_card.py) class implements the [`Dispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/base.py) interface and controls a stepper motor to dispense cards.

## How It Works

When `dispense()` is called, the motor executes a two-phase motion:

1. **Forward stroke** — drives the motor backward (from the motor's perspective) for `dispense_steps` steps, pushing a single card out of the deck
2. **Retract** — drives the motor forward for `retract_steps` steps which is useful to retract a second card which may have been grabbed by the dispense step and pushed slightly forward after the first card was fully dispensed.

## GPIO Pin Wiring

The stepper motor is driven via the ULN2003 board, which connects to four GPIO pins on the Raspberry Pi. The default pin assignments are:

| Config Key | Default GPIO Pin | ULN2003 Input |
|---|---|---|
| `pin_1` | `D17` | IN1 |
| `pin_2` | `D18` | IN2 |
| `pin_3` | `D27` | IN3 |
| `pin_4` | `D22` | IN4 |

### Key Descriptions

| Key | Default | Description |
|---|---|---|
| `pin_1` – `pin_4` | `D17`, `D18`, `D27`, `D22` | GPIO pins connected to the ULN2003 IN1–IN4 inputs |
| `dispense_steps` | `2048` | Number of stepper steps for the forward card-push stroke. 2048 steps = one full revolution of the 28BYJ-48 in half-step mode. Adjust if your printed mechanism needs more or less travel. |
| `retract_steps` | `512` | Number of steps to retract after dispensing. Reduces drag on the remaining deck and prevents double-feeds. |
| `step_delay` | `0.002` | Delay in seconds between each motor step. Lower values = faster motor movement. Going too low may cause the motor to stall. |
| `dispense_delay` | `1.0` | *(Base Dispenser)* Seconds to wait between dispenses when multiple cards are requested. Defined in the base `Dispenser` class and applies to all dispenser types. |

## Configuration

The dispenser is configured via `config.yml` under the `dispenser.gs_card` namespace. All keys are optional — the defaults listed below will be used if a key is absent.

```yaml
dispenser:
  dispense_delay: 1.0       # seconds between dispenses when count > 1 item being dispensed (base Dispenser)
  gs_card:
    pin_1: 17             
    pin_2: 18              
    pin_3: 27              
    pin_4: 22              
    dispense_steps: 2048   
    retract_steps: 512     
    step_delay: 0.002     
```

## Methods

### `dispense(count=1)`
Dispenses `count` cards by running the full forward stroke followed by the retract. If more than one card is being dispensed, it will wait `dispense_delay` seconds between each card dispense. This is the method called by the player during the fortune-telling sequence.

### `step(steps)`
Moves the motor backward by an arbitrary number of steps. Useful for manual calibration and testing via the `goblin-speaks test` CLI command.
