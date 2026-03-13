"""
Game Arcadia Launcher — sub-menu that lists and dispatches to available games.

To register a new game, simply add an instance to the GAMES list below.
"""

from core.settings import Colors
from core.menu import display_menu, get_choice
from core.utils import clear_screen

# ── Import game classes here ─────────────────────────────────────────────────
from game_arcadia.games.number_guessing import NumberGuessingGame

# ── Register games here (order = menu order) ─────────────────────────────────
GAMES = [
    NumberGuessingGame(),
    # Add new games below, e.g.:
    # RockPaperScissorsGame(),
    # TicTacToeGame(),
]


def launch() -> None:
    """Display the Game Arcadia sub-menu and run chosen games."""
    while True:
        clear_screen()

        print(f"\n  {Colors.MAGENTA}{Colors.BOLD}🕹️  GAME ARCADIA{Colors.RESET}")
        print(f"  {Colors.DIM}Choose a game to play!\n{Colors.RESET}")

        # Build menu options from registered games
        options = []
        for i, game in enumerate(GAMES, start=1):
            options.append({
                "key": str(i),
                "label": f"{game.get_name()}  {Colors.DIM}— {game.get_description()}{Colors.RESET}",
            })
        options.append({"key": "b", "label": "Back to Main Menu"})

        display_menu("Game Arcadia", options)
        choice = get_choice(options)

        if choice == "b":
            return  # back to main menu

        # Dispatch to chosen game
        idx = int(choice) - 1
        if 0 <= idx < len(GAMES):
            GAMES[idx].start()
