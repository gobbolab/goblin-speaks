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

## 3D Model Files

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

## Software Implementation

The dispenser is powered by the `GSCardDispenser` software component.

[Read more about the GSCardDispenser Class](../software/components/gs-card.md)