"""
Number Guessing Game — an enhanced Game Arcadia experience.

Features
--------
• Three difficulty levels (Easy / Medium / Hard)
• Custom or preset number ranges
• Dynamic attempt limits based on optimal binary-search depth
• Live visual progress bar showing remaining attempts
• Smart hints ("Even / Odd", "Divisible by …", proximity indicators)
• Win streak tracking within a session
• Colourful, polished terminal UI
"""

import math
import random
from core.settings import Colors
from core.utils import clear_screen, pause
from game_arcadia.games.base_game import BaseGame


# ── Difficulty presets ────────────────────────────────────────────────────────
DIFFICULTIES = {
    "1": {"label": "Easy",   "range": (1, 50),   "extra_attempts": 3, "hints": True},
    "2": {"label": "Medium", "range": (1, 100),  "extra_attempts": 1, "hints": True},
    "3": {"label": "Hard",   "range": (1, 500),  "extra_attempts": 0, "hints": False},
    "4": {"label": "Custom", "range": None,       "extra_attempts": 1, "hints": True},
}


class NumberGuessingGame(BaseGame):
    """Guess a secret number with style — multiple difficulties & smart hints."""

    def __init__(self) -> None:
        self._streak: int = 0        # consecutive wins this session
        self._games_played: int = 0
        self._total_wins: int = 0

    # ── BaseGame interface ────────────────────────────────────────────────
    def get_name(self) -> str:
        return "Number Guessing Game"

    def get_description(self) -> str:
        return "Guess the secret number — with difficulty levels, hints & streaks!"

    def start(self) -> None:
        """Main entry point — shows menu, plays rounds, offers replay."""
        while True:
            clear_screen()
            self._print_header()
            diff = self._choose_difficulty()
            if diff is None:
                return  # back to arcade

            low, high = diff["range"]
            max_attempts = self._calc_max_attempts(low, high) + diff["extra_attempts"]
            show_hints = diff["hints"]

            won = self._play_round(low, high, max_attempts, show_hints)
            self._games_played += 1
            if won:
                self._streak += 1
                self._total_wins += 1
            else:
                self._streak = 0

            self._show_session_stats()

            if not self._ask_replay():
                return

    # ── UI helpers ────────────────────────────────────────────────────────
    @staticmethod
    def _print_header() -> None:
        print()
        print(f"  {Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════╗{Colors.RESET}")
        print(f"  {Colors.CYAN}{Colors.BOLD}║       🎯  NUMBER GUESSING GAME          ║{Colors.RESET}")
        print(f"  {Colors.CYAN}{Colors.BOLD}╚══════════════════════════════════════════╝{Colors.RESET}")
        print()

    @staticmethod
    def _progress_bar(remaining: int, total: int, width: int = 20) -> str:
        """Return a coloured bar: ████████░░░░ 5/10"""
        filled = round(width * remaining / total)
        empty = width - filled
        # Colour shifts as attempts run low
        if remaining / total > 0.5:
            colour = Colors.GREEN
        elif remaining / total > 0.25:
            colour = Colors.YELLOW
        else:
            colour = Colors.RED
        bar = f"{colour}{'█' * filled}{Colors.DIM}{'░' * empty}{Colors.RESET}"
        return f"  {bar}  {remaining}/{total} attempts left"

    # ── Difficulty selection ──────────────────────────────────────────────
    def _choose_difficulty(self) -> dict | None:
        print(f"  {Colors.BOLD}Choose Difficulty:{Colors.RESET}\n")
        print(f"    {Colors.GREEN}[1]{Colors.RESET} Easy    — numbers   1 – 50   (generous attempts + hints)")
        print(f"    {Colors.YELLOW}[2]{Colors.RESET} Medium  — numbers   1 – 100  (fair attempts + hints)")
        print(f"    {Colors.RED}[3]{Colors.RESET} Hard    — numbers   1 – 500  (tight attempts, no hints)")
        print(f"    {Colors.MAGENTA}[4]{Colors.RESET} Custom  — pick your own range!")
        print(f"    {Colors.DIM}[b]{Colors.RESET} Back\n")

        while True:
            choice = input(f"  {Colors.CYAN}▸ {Colors.RESET}").strip().lower()
            if choice == "b":
                return None
            if choice in DIFFICULTIES:
                diff = dict(DIFFICULTIES[choice])  # shallow copy
                if diff["range"] is None:
                    diff["range"] = self._get_custom_range()
                    if diff["range"] is None:
                        return None  # user cancelled
                    # recalculate extra based on range size
                return diff
            print(f"  {Colors.RED}Invalid choice — enter 1, 2, 3, 4, or b.{Colors.RESET}")

    @staticmethod
    def _get_custom_range() -> tuple[int, int] | None:
        """Prompt the user for a custom number range."""
        print()
        try:
            low = int(input(f"  {Colors.CYAN}Lower bound: {Colors.RESET}"))
            high = int(input(f"  {Colors.CYAN}Upper bound: {Colors.RESET}"))
        except ValueError:
            print(f"  {Colors.RED}Please enter valid integers.{Colors.RESET}")
            pause()
            return None
        if low >= high:
            print(f"  {Colors.RED}Upper bound must be greater than lower bound.{Colors.RESET}")
            pause()
            return None
        return (low, high)

    # ── Core game math ────────────────────────────────────────────────────
    @staticmethod
    def _calc_max_attempts(low: int, high: int) -> int:
        """Optimal attempts = ceil(log₂(range_size)), at least 1."""
        return max(1, math.ceil(math.log2(high - low + 1)))

    # ── Game round ────────────────────────────────────────────────────────
    def _play_round(self, low: int, high: int, max_attempts: int, show_hints: bool) -> bool:
        """Run one guessing round. Returns True if the player wins."""
        clear_screen()
        secret = random.randint(low, high)
        attempts = 0

        print()
        print(f"  {Colors.CYAN}{Colors.BOLD}🎯  NUMBER GUESSING GAME{Colors.RESET}")
        print(f"  {Colors.DIM}I picked a number between {Colors.BOLD}{low}{Colors.RESET}"
              f"{Colors.DIM} and {Colors.BOLD}{high}{Colors.RESET}{Colors.DIM}.{Colors.RESET}")
        print(f"  {Colors.DIM}You have {Colors.BOLD}{max_attempts}{Colors.RESET}"
              f"{Colors.DIM} attempts. Good luck!{Colors.RESET}")
        if show_hints:
            print(f"  {Colors.DIM}💡 Hints are ON — pay attention to the clues!{Colors.RESET}")
        print()

        while attempts < max_attempts:
            remaining = max_attempts - attempts
            print(self._progress_bar(remaining, max_attempts))

            # ── get valid integer input ──
            try:
                raw = input(f"\n  {Colors.YELLOW}▸ Your guess: {Colors.RESET}").strip()
                if raw.lower() == "q":
                    print(f"\n  {Colors.DIM}Round abandoned. The number was {Colors.BOLD}{secret}{Colors.RESET}.")
                    pause()
                    return False
                guess = int(raw)
            except ValueError:
                print(f"  {Colors.RED}⚠  Enter a valid number (or 'q' to quit).{Colors.RESET}")
                continue

            if guess < low or guess > high:
                print(f"  {Colors.RED}⚠  Out of range! Guess between {low} and {high}.{Colors.RESET}")
                continue

            attempts += 1

            # ── Check guess ──
            if guess == secret:
                self._celebrate(attempts, max_attempts)
                return True
            elif guess < secret:
                diff_abs = secret - guess
                proximity = self._proximity_label(diff_abs, high - low)
                print(f"  {Colors.BLUE}↑ Too low! {proximity}{Colors.RESET}")
            else:
                diff_abs = guess - secret
                proximity = self._proximity_label(diff_abs, high - low)
                print(f"  {Colors.MAGENTA}↓ Too high! {proximity}{Colors.RESET}")

            # ── Optional hint ──
            if show_hints and attempts < max_attempts:
                hint = self._generate_hint(secret, guess, attempts)
                if hint:
                    print(f"  {Colors.DIM}💡 Hint: {hint}{Colors.RESET}")

            print()

        # Out of attempts
        print(f"\n  {Colors.RED}{Colors.BOLD}💀 Out of attempts!{Colors.RESET}")
        print(f"  {Colors.RED}The number was {Colors.BOLD}{secret}{Colors.RESET}.")
        pause()
        return False

    # ── Proximity feedback ────────────────────────────────────────────────
    @staticmethod
    def _proximity_label(diff: int, total_range: int) -> str:
        """Return a proximity word like 'Very close!' based on distance."""
        ratio = diff / total_range
        if ratio < 0.02:
            return f"{Colors.GREEN}🔥 Extremely close!"
        elif ratio < 0.05:
            return f"{Colors.GREEN}Very close!"
        elif ratio < 0.15:
            return "Getting warm…"
        elif ratio < 0.30:
            return "Somewhat far."
        else:
            return "Way off!"

    # ── Hint generator ────────────────────────────────────────────────────
    @staticmethod
    def _generate_hint(secret: int, last_guess: int, attempt: int) -> str:
        """Return a contextual hint string, varying by attempt number."""
        hints: list[str] = []
        if secret % 2 == 0:
            hints.append("The number is even.")
        else:
            hints.append("The number is odd.")

        for d in (3, 5, 7):
            if secret % d == 0:
                hints.append(f"It's divisible by {d}.")

        if secret > last_guess:
            hints.append("Think higher…")
        else:
            hints.append("Think lower…")

        # Rotate through available hints based on attempt
        return hints[attempt % len(hints)]

    # ── Win celebration ───────────────────────────────────────────────────
    @staticmethod
    def _celebrate(attempts: int, max_attempts: int) -> None:
        """Print a flashy win message."""
        print()
        print(f"  {Colors.GREEN}{Colors.BOLD}╔══════════════════════════════════════════╗{Colors.RESET}")
        print(f"  {Colors.GREEN}{Colors.BOLD}║       🎉  C O R R E C T !  🎉          ║{Colors.RESET}")
        print(f"  {Colors.GREEN}{Colors.BOLD}╚══════════════════════════════════════════╝{Colors.RESET}")
        print(f"  {Colors.GREEN}You nailed it in {Colors.BOLD}{attempts}{Colors.RESET}"
              f"{Colors.GREEN} attempt{'s' if attempts != 1 else ''}!{Colors.RESET}")
        if attempts == 1:
            print(f"  {Colors.YELLOW}{Colors.BOLD}⭐  FIRST TRY — Legendary!{Colors.RESET}")
        elif attempts <= max_attempts // 2:
            print(f"  {Colors.YELLOW}⭐  Impressive guessing!{Colors.RESET}")
        pause()

    # ── Session stats ─────────────────────────────────────────────────────
    def _show_session_stats(self) -> None:
        """Display stats for the current play session."""
        print()
        print(f"  {Colors.DIM}{'─' * 42}{Colors.RESET}")
        print(f"  {Colors.BOLD}📊 Session Stats{Colors.RESET}")
        print(f"     Games played : {Colors.CYAN}{self._games_played}{Colors.RESET}")
        print(f"     Wins         : {Colors.GREEN}{self._total_wins}{Colors.RESET}")
        win_rate = (self._total_wins / self._games_played * 100) if self._games_played else 0
        print(f"     Win rate     : {Colors.YELLOW}{win_rate:.0f}%{Colors.RESET}")
        if self._streak >= 2:
            print(f"     🔥 Win streak : {Colors.RED}{Colors.BOLD}{self._streak}{Colors.RESET}")
        print(f"  {Colors.DIM}{'─' * 42}{Colors.RESET}")

    # ── Replay prompt ─────────────────────────────────────────────────────
    @staticmethod
    def _ask_replay() -> bool:
        """Ask if the player wants another round."""
        print()
        choice = input(f"  {Colors.CYAN}Play again? [y/n]: {Colors.RESET}").strip().lower()
        return choice in ("y", "yes")
