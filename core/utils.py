"""
Shared utility / helper functions used across GameHub.
"""

import os
import sys
from core.settings import Colors, APP_NAME, VERSION, MENU_WIDTH


def clear_screen() -> None:
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def pause(prompt: str = "Press Enter to continue...") -> None:
    """Pause execution until the user presses Enter."""
    input(f"\n{Colors.DIM}{prompt}{Colors.RESET}")


def print_centered(text: str, width: int = MENU_WIDTH, fill: str = " ") -> str:
    """Return *text* centered within *width* characters."""
    return text.center(width, fill)


def print_banner() -> None:
    """Display the GameHub ASCII banner from assets/banner.txt, or a fallback."""
    banner_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "banner.txt")

    if os.path.exists(banner_path):
        with open(banner_path, "r", encoding="utf-8") as f:
            print(f"{Colors.CYAN}{f.read()}{Colors.RESET}")
    else:
        # Fallback inline banner
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("  ╔══════════════════════════════════════════════╗")
        print(f"  ║{'G A M E H U B':^46}║")
        print("  ╚══════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")

    print(f"{Colors.DIM}  v{VERSION}{Colors.RESET}\n")
