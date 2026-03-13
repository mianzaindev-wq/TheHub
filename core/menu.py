"""
Reusable menu renderer and input handler for GameHub.
"""

from core.settings import (
    Colors, MENU_WIDTH, DIVIDER_CHAR,
    BORDER_CHAR_V, CORNER_TL, CORNER_TR,
    CORNER_BL, CORNER_BR, TEE_LEFT, TEE_RIGHT,
)


def _box_top() -> str:
    return f"  {CORNER_TL}{DIVIDER_CHAR * (MENU_WIDTH - 2)}{CORNER_TR}"


def _box_bottom() -> str:
    return f"  {CORNER_BL}{DIVIDER_CHAR * (MENU_WIDTH - 2)}{CORNER_BR}"


def _box_divider() -> str:
    return f"  {TEE_LEFT}{DIVIDER_CHAR * (MENU_WIDTH - 2)}{TEE_RIGHT}"


def _box_row(text: str, color: str = "") -> str:
    inner = f" {text}"
    padding = MENU_WIDTH - 2 - len(inner)
    return f"  {BORDER_CHAR_V}{color}{inner}{' ' * max(padding, 0)}{Colors.RESET}{BORDER_CHAR_V}"


def display_menu(title: str, options: list[dict]) -> None:
    """
    Render a styled box menu in the terminal.

    Parameters
    ----------
    title : str
        Header shown at the top of the menu box.
    options : list[dict]
        Each dict must have ``key`` (display label, e.g. "1") and ``label``.
    """
    print(_box_top())
    print(_box_row(title.upper(), Colors.BOLD + Colors.CYAN))
    print(_box_divider())

    for opt in options:
        label = f"[{opt['key']}]  {opt['label']}"
        print(_box_row(label, Colors.YELLOW))

    print(_box_bottom())


def get_choice(options: list[dict]) -> str:
    """
    Prompt for input and validate against the given options.

    Returns the matched ``key`` string (lower-cased).
    """
    valid_keys = {str(opt["key"]).lower() for opt in options}

    while True:
        choice = input(f"\n  {Colors.GREEN}▶ Enter your choice: {Colors.RESET}").strip().lower()
        if choice in valid_keys:
            return choice
        print(f"  {Colors.RED}✖ Invalid choice. Please try again.{Colors.RESET}")
