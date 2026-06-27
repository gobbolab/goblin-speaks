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
| 1 | 3D printed dispenser body | See model link above |
| 1 | 3D printed dispenser back | See model link above |
| 1 | 3D printed o-ring wheel | See model link above |
| 1 | 28BYJ-48 Stepper Motor | 5V, commonly sold with ULN2003 driver |
| 1 | ULN2003 Stepper Motor Driver Board | Usually bundled with the motor |
| 6 | Dupont jumper wires | For connecting driver board to GPIO pins |
| 2 | M3 Heat-set Inserts | For mounting the motor to the printed body |
| 2 | M3 screws | For mounting the motor to the printed body |
| 2 | 25mm x 2.4mm (Inner Diameter x Cross Section) Rubber O-rings | For friction on the card dispenser wheel |

---

## Build Steps

1. Glue the back to the main dispenser body. Ensure it is facing the right way, the side of the dispenser with the tab is the top. The tab on the back should slide underneath the dispenser card tray.
2. Use a soldering iron to insert the 2 M3 Heat-set inserts into the holes on the side of the dispenser.
3. Slide the two o-rings into the indented slots on the o-ring wheel.
4. Slide the o-ring wheel onto the shaft of the stepper motor.
5. Use the M3 screws to attach the stepper motor to the dispenser by threading them into the heat-set insterts.
6. Place a card into the hopper of the dispenser and slide it out the gate over the o-ring wheel by pressing with two fingers on the rear of the dispenser and pushing forward. You should be able to push the card under the gate and feel tension as you pull it through. If the card won't move through the gate at all, you need to lower the motor position.
7. Run a few tests of the dispenser to check tension. If the tension is too tight, a card wont be able to make it through the gate. If the tension is two low, multiple cards might pass the gate at the same time.

---

## Software Implementation

The dispenser is powered by the `GSCardDispenser` software component.

[Read more about the GSCardDispenser Class](../software/components/gs-card.md)