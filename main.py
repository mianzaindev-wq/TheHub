"""
GameHub — Main Entry Point
Run this file to start the application: python main.py
"""

from core.settings import Colors
from core.menu import display_menu, get_choice
from core.utils import clear_screen, print_banner
from game_arcadia import launcher as arcadia_launcher


def main() -> None:
    """Main application loop — renders the top-level menu."""
    while True:
        clear_screen()
        print_banner()

        options = [
            {"key": "1", "label": "🕹️  Game Arcadia"},
            # ── Add new sections below ────────────────────────────────
            # {"key": "2", "label": "📊  Leaderboards"},
            # {"key": "3", "label": "⚙️  Settings"},
            {"key": "q", "label": "🚪  Quit"},
        ]

        display_menu("Main Menu", options)
        choice = get_choice(options)

        if choice == "1":
            arcadia_launcher.launch()
        # elif choice == "2":
        #     leaderboard_launcher.launch()
        elif choice == "q":
            clear_screen()
            print(f"\n  {Colors.CYAN}Thanks for using GameHub! Goodbye 👋{Colors.RESET}\n")
            break


if __name__ == "__main__":
    main()
