"""
Global settings and constants for GameHub.
"""

# ── App Info ──────────────────────────────────────────────────────────────────
APP_NAME = "GameHub"
VERSION = "1.0.0"
AUTHOR = "Zain"

# ── Terminal Colours (ANSI) ───────────────────────────────────────────────────
class Colors:
    """ANSI escape codes for terminal styling."""
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Foreground
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    # Backgrounds
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"

# ── Menu Styling ──────────────────────────────────────────────────────────────
MENU_WIDTH = 50          # character width of menu boxes
DIVIDER_CHAR = "═"       # character used for horizontal dividers
BORDER_CHAR_V = "║"      # vertical border
CORNER_TL = "╔"
CORNER_TR = "╗"
CORNER_BL = "╚"
CORNER_BR = "╝"
TEE_LEFT = "╠"
TEE_RIGHT = "╣"
