"""
Abstract base class that every Game Arcadia game must implement.

To create a new game:
1. Create a new .py file in this directory.
2. Subclass BaseGame.
3. Implement get_name(), get_description(), and start().
4. Register the game in game_arcadia/launcher.py's GAMES list.
"""

from abc import ABC, abstractmethod


class BaseGame(ABC):
    """Blueprint for all mini-games in Game Arcadia."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of the game."""
        ...

    @abstractmethod
    def get_description(self) -> str:
        """Return a short one-line description of the game."""
        ...

    @abstractmethod
    def start(self) -> None:
        """Run the game loop. Control returns here when the game ends."""
        ...

    def __repr__(self) -> str:
        return f"<Game: {self.get_name()}>"
