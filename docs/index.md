---
layout: default
title: Home
description: Goblin Speaks Penny Arcade Framework documentation home.
---

# Goblin Speaks Penny Arcade Framework

**An open source framework for building your own penny arcade amusement machine on Raspberry Pi.**

Whether you're building a fortune teller, an animatronic show, an interactive game, or something else entirely, Goblin Speaks gives you the building blocks to do it.
The project is inspired by vintage penny arcade machines and fortune teller machines.
It gets its name from the first machine built using the framework, the Goblin Speaks fortune teller.

![Gypsy grandma machine](images/gypsy-grandma.jpg)

## How It Works

A Goblin Speaks machine is assembled from a set of component types, each built behind a common interface so they can be mixed, matched, or replaced:

- **Activators** trigger the show — a coin reader, a button, a motion sensor.
- **Animatronics** bring the machine to life — articulating mouths, arms, heads.
- **Dispensers** hand the player a physical reward — a fortune card, token, or toy.
- **Audio** plays narration, sound effects, and music throughout the show.

You wire these together in a single config file (`/etc/goblin-speaks/config.yml`) that declares which components make up your machine and the sequence of actions to run each time it's activated.
The framework provides several ready to use components like animatronic character frames, coin readers and card dispensers.
Most likely your unique machine will require some components that are not provided directly by the framework.
The framework provides a plugin system, allowing you to write a Python file implementing the component's interface — drop it in the plugins directory, and reference it from your config; no need to touch the framework source itself.

[Read more about the Software](software/overview.md) · [Read more about Components](components/overview.md)

## See it in Action

The framework's namesake machine, the Goblin Speaks fortune teller, is a fortune telling cabinet built entirely from the framework's components: a [Goblin Speaks Body](components/goblin-speaks-animatronic-body.md) and [Head](components/goblin-speaks-head.md) animate as the machine speaks, and a [Card Dispenser](components/goblin-speaks-card-dispenser.md) hands the player a fortune card at the end of the show.

[See how the Goblin Speaks machine works](goblin-speaks-example.md)

## Get Involved

- **Complete a machine** — builders who finish a machine using the framework can apply for a [serial number](serial-numbers.md).
- **Design a component** — built your own component for the framework? Open a PR to link it from the [Components Overview](components/overview.md).

[Browse the code on GitHub](https://github.com/gobbolab/goblin-speaks)