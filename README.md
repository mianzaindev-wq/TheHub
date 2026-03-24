# 🎮 GameHub

A scalable, modular Python application that brings together multiple interactive experiences under one terminal-based menu

## ✨ Features

| Module | Description |
|--------|-------------|
| **Game Arcadia** | A collection of mini-games you can launch from the terminal |

### 🕹️ Available Games

| Game | Type | Description |
|------|------|-------------|
| **Number Guessing** | Terminal | Guess the secret number — multiple difficulty levels, smart hints & win streaks |
| **Flappy Bird** | Pygame (GUI) | Navigate through pipes — a classic arcade challenge! |

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- **pygame** (required only for Flappy Bird)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run
```bash
python main.py
```

### Run Tests
```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
GameHub/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── core/                        # Shared utilities & menu system
│   ├── menu.py                  # Reusable menu renderer
│   ├── settings.py              # Global constants & colours
│   └── utils.py                 # Helper functions
├── game_arcadia/                # Game Arcadia module
│   ├── launcher.py              # Sub-menu & game dispatcher
│   └── games/                   # Individual game modules
│       ├── base_game.py         # Abstract base class
│       ├── number_guessing.py   # Number Guessing Game
│       └── flappy_bird.py       # Flappy Bird (pygame)
├── assets/                      # Static resources
│   ├── banner.txt               # Terminal banner art
│   └── flappy_bird/             # Flappy Bird assets
│       ├── sprites/             # bird, pipes, background, digits…
│       └── audio/               # sound effects (.wav)
└── tests/                       # Unit tests
```

## 🐦 Flappy Bird Assets

Flappy Bird requires sprite and audio assets placed in `assets/flappy_bird/`:

```
assets/flappy_bird/
├── sprites/
│   ├── bird.png
│   ├── background.png
│   ├── base.png
│   ├── pipe.png
│   ├── message.png
│   └── 0.png – 9.png        # digit sprites for the score display
└── audio/
    ├── die.wav
    ├── hit.wav
    ├── point.wav
    ├── swoosh.wav
    └── wing.wav
```

> **Note:** If asset files are missing, the game will display a friendly error message instead of crashing.

## ➕ Adding a New Game

1. Create a new file in `game_arcadia/games/`, e.g. `my_game.py`.
2. Subclass `BaseGame` and implement `get_name()`, `get_description()`, and `start()`.
3. Import and register your game in `game_arcadia/launcher.py`:
   ```python
   from game_arcadia.games.my_game import MyGame
   GAMES = [
       NumberGuessingGame(),
       FlappyBirdGame(),
       MyGame(),  # ← add here
   ]
   ```
4. Done — it appears in the Game Arcadia menu automatically!

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
