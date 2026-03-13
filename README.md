# 🎮 GameHub

A scalable, modular Python application that brings together multiple interactive experiences under one terminal-based menu.

## ✨ Features

| Module | Description |
|--------|-------------|
| **Game Arcadia** | A collection of mini-games — currently includes the *Number Guessing Game* |
| *More coming soon…* | Leaderboards, Settings, and more |

## 🚀 Getting Started

### Prerequisites
- Python 3.10+

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
├── main.py                  # Entry point
├── core/                    # Shared utilities & menu system
│   ├── menu.py              # Reusable menu renderer
│   ├── settings.py          # Global constants & colours
│   └── utils.py             # Helper functions
├── game_arcadia/            # Game Arcadia module
│   ├── launcher.py          # Sub-menu & game dispatcher
│   └── games/               # Individual game modules
│       ├── base_game.py     # Abstract base class
│       └── number_guessing.py
├── assets/                  # Static resources (banners, etc.)
└── tests/                   # Unit tests
```

## ➕ Adding a New Game

1. Create a new file in `game_arcadia/games/`, e.g. `my_game.py`.
2. Subclass `BaseGame` and implement `get_name()`, `get_description()`, and `start()`.
3. Import and register your game in `game_arcadia/launcher.py`:
   ```python
   from game_arcadia.games.my_game import MyGame
   GAMES = [
       NumberGuessingGame(),
       MyGame(),  # ← add here
   ]
   ```
4. Done — it appears in the Game Arcadia menu automatically!

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
