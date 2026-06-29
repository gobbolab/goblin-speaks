---
layout: default
title: Plugins
description: How to create and use plugins to extend the Goblin Speaks framework with custom components.
---

# Plugins

The Goblin Speaks framework supports plugins for all core component types: **Dispensers**, **Animatronics**, and **Activators**. Plugins let you create your own custom components and use them in your machine without modifying the framework source code.

## How Plugins Work

When a factory creates a component, it follows this order:

1. **Built-in components** are checked first (e.g., `single_stepper`, `gs_body`, `gs_button`)
2. **Plugins** are checked if no built-in component matches the requested type

Plugins are discovered automatically by scanning a plugins directory for Python files. Each file should contain a class that extends the appropriate abstract base class for its component type.

## Plugin Directory

By default, plugins are loaded from:

```
~/.goblin-speaks/plugins/
```

Inside this directory, create a subdirectory for each component type you want to extend:

```
~/.goblin-speaks/plugins/
    dispenser/
    activator/
    animatronic/
```

You only need to create subdirectories for the component types you're adding plugins for.

### Custom Plugin Directory

You can change the plugins directory in your `config.yml`:

```yaml
plugins:
  directory: /path/to/your/plugins
```

## Creating a Plugin

A plugin is a single `.py` file placed in the appropriate component type subdirectory. The **filename** (without the `.py` extension) becomes the name you use to reference the plugin in your configuration.

The framework automatically provides the base class and `Config` to your plugin — you do not need to import them. They are injected into the plugin's namespace before it runs.

Each plugin file must contain a class that:

- Extends the correct abstract base class (`Dispenser`, `Activator`, or `Animatronic`)
- Implements all required abstract methods
- Accepts `config_prefix=None` as a constructor parameter

### Component Interfaces

| Component Type | Base Class | Required Methods |
|---------------|-----------|-----------------|
| Dispenser | `Dispenser` | `_dispense_one()` |
| Activator | `Activator` | `start(callback)`, `shutdown()` |
| Animatronic | `Animatronic` | `animate(duration)`, `test()` |

## CLI

The `goblin-speaks plugin` command creates a new plugin skeleton file with the correct directory structure and method stubs already in place.

```
goblin-speaks plugin <component_type> <name>
```

- `component_type` — one of `dispenser`, `activator`, or `animatronic`
- `name` — the snake_case name for your plugin (this becomes the filename and the config key)

The skeleton is generated programmatically from the base class, so it will always include the correct abstract methods and their signatures.

## Tutorial: Creating a Dispenser Plugin

This walkthrough creates a minimal dispenser plugin to show the basics.

### Step 1: Generate the Skeleton

```bash
goblin-speaks plugin dispenser my_dispenser
```

This creates the plugin directory and skeleton file automatically:

```
Created plugin skeleton: ~/.goblin-speaks/plugins/dispenser/my_dispenser.py
```

The generated file will look like this:

```python
class MyDispenser(Dispenser):
    def __init__(self, config_prefix=None):
        super().__init__(config_prefix)
        print("TODO: initialize MyDispenser")

    def _dispense_one(self):
        print("TODO: implement _dispense_one")
```

### Step 2: Update Your Config

In your `/etc/goblin-speaks/config.yml`, reference the plugin by its filename:

```yaml
components:
  my_prize_dispenser:
    type: dispenser
    class: my_dispenser
```

The `class: my_dispenser` value matches the filename `my_dispenser.py`.

### Step 3: Use It

Run your machine as usual. The framework will find the built-in dispensers first, and when it doesn't find `my_dispenser` among them, it will load it from your plugins directory.

```bash
goblin-speaks run
```

You should see output like:

```
Loaded plugin: my_dispenser (MyDispenser)
Creating component 'my_prize_dispenser' (type: dispenser, class: my_dispenser)
```

## Tips

- **One class per file.** The plugin loader uses the first subclass of the base class it finds in each file. Additional classes are ignored.
- **Files starting with `_` are skipped.** Use this for helper modules that shouldn't be loaded as plugins (e.g., `_utils.py`).
- **Errors don't crash the app.** If a plugin fails to load, a warning is printed and the plugin is skipped. Other plugins and built-in components are unaffected.
- **Plugins are cached.** The plugin directory is only scanned once per component type per application run. If you add a new plugin, restart the application.
