---
layout: default
title: CLI
description: Command-line interface reference for the Goblin Speaks software.
---

# CLI

The Goblin Speaks software uses [typer](https://typer.tiangolo.com/) to provide a command-line interface. The CLI is the primary way to interact with the machine.

## Commands

### `run`

Starts the machine and begins the main play loop.

```bash
goblin-speaks run
```

### `test`

Launches an interactive test menu that lets you test individual components without running a full play sequence. The menu dynamically lists all components loaded from your config and allows you to:

- Play the full sequence
- Test each animatronic
- Test each dispenser
- Test audio playback
- Test each activator (waits for a trigger event)

```bash
goblin-speaks test
```

### `update`

Pulls the latest release of Goblin Speaks from GitHub and runs the installer script. After a successful update, the process exits so that systemd can restart it with the new version.

```bash
goblin-speaks update
```

### `plugin`

Generates a skeleton plugin file for a given component type. This creates a new Python file in the plugins directory with stub implementations of all required abstract methods.

```bash
goblin-speaks plugin <component_type> <name>
```

**Arguments:**

| Argument | Description |
|---|---|
| `component_type` | The type of component to create. One of: `dispenser`, `activator`, `animatronic` |
| `name` | The name for the plugin in snake_case (e.g. `my_dispenser`) |

**Example:**

```bash
goblin-speaks plugin dispenser my_card_dispenser
```

This creates a file at `/etc/goblin-speaks/plugins/dispenser/my_card_dispenser.py` with a `MyCardDispenser` class that extends `Dispenser` and includes stubs for all required methods.
