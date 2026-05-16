# Arkanoid

A Python Arkanoid game built with pygame. Graphics and music are 100% procedurally generated — no external assets.

## Features

- Ball, paddle and bricks with procedural visual effects (gradients, destruction animation)
- Two animated backgrounds: scrolling grid (`grid`) and perspective tunnel (`trench`)
- Synthwave music generated entirely by code (bass, arpeggio, pad)
- Pause with music synchronization
- Gamepad support (axis 0 + button 1)
- Debug speed control: x1 to x16, current multiplier displayed on screen

## Controls

### Keyboard

| Key | Action |
|-----|--------|
| `←` / `→` | Move paddle |
| `Space` | Launch ball |
| `p` | Pause / Resume |
| `>` | Speed up (x1 → x2 → x4 → x8 → x16) |
| `<` | Speed down |

### Gamepad

| Input | Action |
|-------|--------|
| Left stick (axis 0) | Move paddle |
| Button 1 | Launch ball |

## Getting started

### Prerequisites

- Python 3.13+
- [Poetry](https://python-poetry.org/docs/#installation)

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

### Install

```bash
git clone <repo>
cd arkanoid
poetry install
```

### Run

```bash
poetry run play          # grid background (default)
poetry run play-trench   # perspective background
```

## Project structure

```
src/game/
├── arkadoid.py          # main loop
├── domain/              # game logic (no pygame)
│   └── entities.py      # Ball, Paddle, Brick, BrickWall
├── graphics/            # rendering
│   └── renderer.py      # Renderer + backgrounds
├── input/               # input handling
│   └── handler.py       # InputHandler
└── audio/               # procedural music
    ├── synth.py          # oscillators + ADSR (numpy)
    ├── composer.py       # loop composition
    └── player.py         # AudioPlayer
```

## Configuration

The `BACKGROUND` constant in `src/game/arkadoid.py` sets the default background:

```python
BACKGROUND = "grid"  # "grid" | "trench"
```
