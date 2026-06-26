---
layout: default
title: Contributing
description: Details on how to contribute to the Goblin Speaks project.
---

# Contributing

The framework is designed to be modular and moddable, allowing you to design and integrate your own components.
Pull requests are welcome for new component types or improvements to existing ones.
There are currently two types of components in the framework:

**Hardware Components**: These represent physical hardware devices connected to the machine.

   - Animatronics (Animated armatures for characters and creatures in the machine)
   - Dispensers (Used to dispense fortune cards or other objects)

**Software Components**: These manage the logic and flow of the machine entirely in software.

   - Players (Orchestrators that combine audio, animatronics, and dispensers to execute the fortune telling sequence)

## Adding a New Animatronic Implementation

To add a new animatronic type:

1. Create a new class that extends the `Animatronic` base class
2. Implement the `animate(duration)` and `test()` methods
3. Register it in the `AnimatronicFactory` in `src/animatronic/factory.py`
4. Update your `goblin-speaks-config.yml` to specify the new type

## Adding a New Dispenser Implementation

To add a new dispenser type:

1. Create a new class that extends the `Dispenser` base class
2. Implement the `dispense()` and `test()` methods
3. Register it in the `DispenserFactory` in `src/dispenser/factory.py`
4. Update your `goblin-speaks-config.yml` to specify the new type

This modular architecture makes it easy to experiment with different hardware configurations and implementations.
