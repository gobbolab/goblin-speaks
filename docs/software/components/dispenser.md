---
layout: default
title: Dispenser Interface
description: Details on the Dispenser abstract base class.
---

# `Dispenser` Interface

The [`Dispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/base.py) interface provides the core abstraction for all dispensers in the Goblin Speaks framework. 

All specific dispenser implementations (like the `SingleStepperDispenser`) must inherit from this abstract base class and implement its required methods.

## Template Method: `dispense(count=1)`

The `Dispenser` base class provides a concrete `dispense()` method which handles the logic for dispensing multiple items. 

If `count` is greater than 1, it will loop `count` times, calling the abstract `_dispense_one()` method on each iteration, and pausing for `dispense_delay` seconds between each item. 

## Required Methods

Custom implementations must provide the following method:

### `_dispense_one()`
Performs the actual hardware action to dispense a single item. This is called internally by the `dispense()` template method.

## Configuration

The base `Dispenser` class reads `dispense_delay` from the component's config prefix. When a component is declared in the `components` section (the normal case), this key lives directly under that component's entry:

```yaml
components:
  card_dispenser:
    type: dispenser
    class: single_stepper
    dispense_delay: 1.0
```

| Config Key | Default | Description |
|---|---|---|
| `dispense_delay` | `1.0` | Number of seconds to pause between dispenses if the player calls `dispense(count)` where `count` is greater than 1. |
