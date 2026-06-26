---
layout: default
title: Goblin Speaks Card Dispenser
description: A 3D-printable stepper motor card dispenser designed to dispense standard poker-sized cards for the Goblin Speaks Fortune Teller framework.
---

# Goblin Speaks Card Dispenser

The Goblin Speaks Card Dispenser is a 3D-printable hardware component designed to reliably dispense single cards from a loaded deck. It is sized for **standard poker-sized cards** (63 × 88 mm), the same sized used by games like Magic: The Gathering and Pokemon. There are plenty of printing services out there which can print custom poker sized cards, allowing you to design and dispense your own custom fortune cards.

The dispenser is driven by a **28BYJ-48 stepper motor** controlled by a **ULN2003 driver board**.

The dispenser integrates directly with the Goblin Speaks framework via the [`GSCardDispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/gs_card.py) class.

---

## 3D Model

The printable model for the card dispenser is available on Printables:

> 🔗 **[Goblin Speaks Card Dispenser — Printables](#)** *(link coming soon)*

---

## Bill of Materials

| Qty | Part | Notes |
|-----|------|-------|
| 1 | 28BYJ-48 Stepper Motor | 5V, commonly sold with ULN2003 driver |
| 1 | ULN2003 Stepper Motor Driver Board | Usually bundled with the motor |
| 6 | Dupont jumper wires | For connecting driver board to GPIO pins |
| 1 | 3D printed dispenser body | See model link above |
| 1 | 3D printed dispenser wheel | See model link above |
| 1 | 3D printed dispenser back | See model link above |
| 2 | M3 Heat-set Inserts | For mounting the motor to the printed body |
| 2 | M3 screws | For mounting the motor to the printed body |
| 2 | Nmm Rubber O-rings | For friction on the card dispenser wheel |

---

## Build Steps

> 🚧 **Build instructions coming soon.**

---

## `GSCardDispenser` Class

The [`GSCardDispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/gs_card.py) class implements the [`Dispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/base.py) interface and controls the stepper motor to dispense cards.

### How It Works

When `dispense()` is called, the motor executes a two-phase motion:

1. **Forward stroke** — drives the motor backward (from the motor's perspective) for `dispense_steps` steps, pushing a single card out of the deck
2. **Retract** — drives the motor forward for `retract_steps` steps which is useful to retract a second card which may have been grabbed by the dispense step and pushed slightly forward after the first card was fully dispensed.

### GPIO Pin Wiring

The stepper motor is driven via the ULN2003 board, which connects to four GPIO pins on the Raspberry Pi. The default pin assignments are:

| Config Key | Default GPIO Pin | ULN2003 Input |
|---|---|---|
| `pin_1` | `D17` | IN1 |
| `pin_2` | `D18` | IN2 |
| `pin_3` | `D27` | IN3 |
| `pin_4` | `D22` | IN4 |

#### Key Descriptions

| Key | Default | Description |
|---|---|---|
| `pin_1` – `pin_4` | `D17`, `D18`, `D27`, `D22` | GPIO pins connected to the ULN2003 IN1–IN4 inputs |
| `dispense_steps` | `2048` | Number of stepper steps for the forward card-push stroke. 2048 steps = one full revolution of the 28BYJ-48 in half-step mode. Adjust if your printed mechanism needs more or less travel. |
| `retract_steps` | `512` | Number of steps to retract after dispensing. Reduces drag on the remaining deck and prevents double-feeds. |
| `step_delay` | `0.002` | Delay in seconds between each motor step. Lower values = faster motor movement. Going too low may cause the motor to stall. |
| `dispense_delay` | `1.0` | *(Base Dispenser)* Seconds to wait between dispenses when multiple cards are requested. Defined in the base `Dispenser` class and applies to all dispenser types. |

### Configuration

The dispenser is configured via `goblin-speaks-config.yml` under the `dispenser.gs_card` namespace. All keys are optional — the defaults listed below will be used if a key is absent.

```yaml
dispenser:
  dispense_delay: 1.0       # seconds between dispenses when count > 1 (base Dispenser)
  gs_card:
    pin_1: 17             
    pin_2: 18              
    pin_3: 27              
    pin_4: 22              
    dispense_steps: 2048   
    retract_steps: 512     
    step_delay: 0.002     
```

### Methods

#### `dispense()`
Dispenses a single card by running the full forward stroke followed by the retract. This is the method called automatically by the player during the fortune-telling sequence.

#### `step(steps)`
Moves the motor backward by an arbitrary number of steps. Useful for manual calibration and testing via the `goblin-speaks test` CLI command.