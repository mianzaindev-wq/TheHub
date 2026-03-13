"""
Number Guessing Game — a working sample game for Game Arcadia.
"""

import random
from core.settings import Colors
from core.utils import clear_screen, pause
from game_arcadia.games.base_game import BaseGame


class NumberGuessingGame(BaseGame):
    """Guess a random number between 1 and 100."""

    def get_name(self) -> str:
        return "Number Guessing Game"

    def get_description(self) -> str:
        return "Guess the secret number between 1 and 100!"

    def start(self) -> None:
        clear_screen()
        secret = random.randint(1, 100)
        attempts = 0
        max_attempts = 10

        print(f"\n  {Colors.CYAN}{Colors.BOLD}🎯  NUMBER GUESSING GAME{Colors.RESET}")
        print(f"  {Colors.DIM}I'm thinking of a number between 1 and 100.")
        print(f"  You have {max_attempts} attempts. Good luck!{Colors.RESET}\n")

        while attempts < max_attempts:
            remaining = max_attempts - attempts
            try:
                guess = int(input(f"  {Colors.YELLOW}[{remaining} left] Your guess: {Colors.RESET}"))
            except ValueError:
                print(f"  {Colors.RED}Please enter a valid number.{Colors.RESET}")
                continue

            attempts += 1

            if guess < secret:
                print(f"  {Colors.BLUE}↑ Too low!{Colors.RESET}")
            elif guess > secret:
                print(f"  {Colors.MAGENTA}↓ Too high!{Colors.RESET}")
            else:
                print(f"\n  {Colors.GREEN}{Colors.BOLD}🎉 Correct! You guessed it in {attempts} attempt(s)!{Colors.RESET}")
                pause()
                return

        print(f"\n  {Colors.RED}💀 Out of attempts! The number was {Colors.BOLD}{secret}{Colors.RESET}.")
        pause()
