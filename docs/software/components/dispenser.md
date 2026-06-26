---
layout: default
title: Dispenser Interface
description: Details on the Dispenser abstract base class.
---

# `Dispenser` Interface

The [`Dispenser`](https://github.com/gobbolab/goblin-speaks/blob/main/src/dispenser/base.py) interface provides the core abstraction for all dispensers in the Goblin Speaks framework. 

All specific dispenser implementations (like the `GSCardDispenser`) must inherit from this abstract base class and implement its required methods.

## Template Method: `dispense(count=1)`

The `Dispenser` base class provides a concrete `dispense()` method which handles the logic for dispensing multiple items. 

If `count` is greater than 1, it will loop `count` times, calling the abstract `_dispense_one()` method on each iteration, and pausing for `dispense_delay` seconds between each item. 

## Required Methods

Custom implementations must provide the following method:

### `_dispense_one()`
Performs the actual hardware action to dispense a single item. This is called internally by the `dispense()` template method.

## Optional Methods

### `step(steps)`
Moves the dispenser mechanism an arbitrary number of steps. This is useful for manual calibration and testing via the CLI but is not required. It defaults to a no-op if not overridden.

## Configuration

The base dispenser reads the following global configuration values from `config.yml` under the `dispenser` namespace:

```yaml
dispenser:
  type: gs_card
  dispense_delay: 1.0
```

| Config Key | Default | Description |
|---|---|---|
| `type` | `gs_card` | The specific class type to instantiate from the `DispenserFactory`. |
| `dispense_delay` | `1.0` | Number of seconds to pause between dispenses if the player calls `dispense(count)` where `count` is greater than 1. |
