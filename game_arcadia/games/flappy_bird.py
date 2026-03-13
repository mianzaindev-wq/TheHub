"""
Flappy Bird — a pygame-based arcade game for Game Arcadia.

Assets required in ``assets/flappy_bird/``:
    sprites/  — bird.png, background.png, base.png, pipe.png,
                message.png, 0.png – 9.png
    audio/    — die.wav, hit.wav, point.wav, swoosh.wav, wing.wav

The game launches a separate pygame window and returns control to
the terminal menu when the player closes it or presses Escape.
"""

import os
import sys
import random

try:
    import pygame
    from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_UP
except ImportError:
    pygame = None  # handled gracefully in start()

from core.settings import Colors
from core.utils import clear_screen, pause
from game_arcadia.games.base_game import BaseGame

# ── Resolve the asset root relative to the project ──────────────────────────
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
_ASSET_DIR = os.path.join(_PROJECT_ROOT, "assets", "flappy_bird")
_SPRITE_DIR = os.path.join(_ASSET_DIR, "sprites")
_AUDIO_DIR = os.path.join(_ASSET_DIR, "audio")

# ── Game constants ───────────────────────────────────────────────────────────
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
GROUND_Y = SCREEN_HEIGHT * 0.8


class FlappyBirdGame(BaseGame):
    """Flappy Bird clone wrapped in the BaseGame interface."""

    # ── BaseGame interface ────────────────────────────────────────────────
    def get_name(self) -> str:
        return "Flappy Bird"

    def get_description(self) -> str:
        return "Navigate through pipes — a classic arcade challenge!"

    def start(self) -> None:
        """Entry point called by the launcher."""
        # --- Pre-flight checks ------------------------------------------------
        if pygame is None:
            clear_screen()
            print(f"\n  {Colors.RED}{Colors.BOLD}⚠  pygame is not installed!{Colors.RESET}")
            print(f"  {Colors.DIM}Run:  pip install pygame{Colors.RESET}")
            pause()
            return

        if not os.path.isdir(_SPRITE_DIR):
            clear_screen()
            print(f"\n  {Colors.RED}{Colors.BOLD}⚠  Missing Flappy Bird assets!{Colors.RESET}")
            print(f"  {Colors.DIM}Expected sprites in:{Colors.RESET}")
            print(f"    {_SPRITE_DIR}")
            print(f"\n  {Colors.DIM}Expected audio in:{Colors.RESET}")
            print(f"    {_AUDIO_DIR}")
            print(f"\n  {Colors.DIM}See README → Assets section for details.{Colors.RESET}")
            pause()
            return

        # --- Launch the game ---------------------------------------------------
        try:
            self._run_game()
        except Exception as exc:  # noqa: BLE001
            # Ensure pygame shuts down cleanly on any crash
            pygame.quit()
            clear_screen()
            print(f"\n  {Colors.RED}{Colors.BOLD}⚠  Flappy Bird crashed:{Colors.RESET}")
            print(f"  {Colors.DIM}{exc}{Colors.RESET}")
            pause()

    # ── Private: full game loop ───────────────────────────────────────────
    def _run_game(self) -> None:
        """Initialise pygame, load assets, and run the game loop."""
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird — GameHub")

        sprites: dict = {}
        sounds: dict = {}

        # ── Load sprites ──────────────────────────────────────────────────
        sprites["numbers"] = tuple(
            pygame.image.load(os.path.join(_SPRITE_DIR, f"{i}.png")).convert_alpha()
            for i in range(10)
        )
        sprites["message"] = pygame.image.load(
            os.path.join(_SPRITE_DIR, "message.png")
        ).convert_alpha()
        sprites["base"] = pygame.image.load(
            os.path.join(_SPRITE_DIR, "base.png")
        ).convert_alpha()
        sprites["background"] = pygame.image.load(
            os.path.join(_SPRITE_DIR, "background.png")
        ).convert()
        sprites["player"] = pygame.image.load(
            os.path.join(_SPRITE_DIR, "bird.png")
        ).convert_alpha()

        pipe_img = pygame.image.load(
            os.path.join(_SPRITE_DIR, "pipe.png")
        ).convert_alpha()
        sprites["pipe"] = (
            pygame.transform.rotate(pipe_img, 180),  # upper pipe (flipped)
            pipe_img,                                  # lower pipe
        )

        # ── Load sounds ──────────────────────────────────────────────────
        for name in ("die", "hit", "point", "swoosh", "wing"):
            sounds[name] = pygame.mixer.Sound(
                os.path.join(_AUDIO_DIR, f"{name}.wav")
            )

        # ── Main loop: welcome → play → repeat ──────────────────────────
        try:
            while True:
                if not self._welcome_screen(screen, clock, sprites):
                    break  # player closed the window
                if not self._main_game(screen, clock, sprites, sounds):
                    break
        finally:
            pygame.quit()

    # ── Welcome / title screen ────────────────────────────────────────────
    @staticmethod
    def _welcome_screen(screen, clock, sprites) -> bool:
        """Show the title screen. Returns False if the player quits."""
        player_x = int(SCREEN_WIDTH / 5)
        player_y = int((SCREEN_HEIGHT - sprites["player"].get_height()) / 2)
        message_x = int((SCREEN_WIDTH - sprites["message"].get_width()) / 2)
        message_y = int(SCREEN_HEIGHT * 0.13)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    return False
                if event.type == KEYDOWN and event.key in (K_SPACE, K_UP):
                    return True

            screen.blit(sprites["background"], (0, 0))
            screen.blit(sprites["player"], (player_x, player_y))
            screen.blit(sprites["message"], (message_x, message_y))
            screen.blit(sprites["base"], (0, GROUND_Y))
            pygame.display.update()
            clock.tick(FPS)

    # ── Core gameplay ─────────────────────────────────────────────────────
    @staticmethod
    def _main_game(screen, clock, sprites, sounds) -> bool:
        """Run one round of gameplay. Returns False if the player quits."""
        score = 0
        player_x = int(SCREEN_WIDTH / 5)
        player_y = int(SCREEN_WIDTH / 2)

        pipe1 = _get_random_pipe(sprites)
        pipe2 = _get_random_pipe(sprites)

        upper_pipes = [
            {"x": SCREEN_WIDTH + 200, "y": pipe1[0]["y"]},
            {"x": SCREEN_WIDTH + 200 + SCREEN_WIDTH // 2, "y": pipe2[0]["y"]},
        ]
        lower_pipes = [
            {"x": SCREEN_WIDTH + 200, "y": pipe1[1]["y"]},
            {"x": SCREEN_WIDTH + 200 + SCREEN_WIDTH // 2, "y": pipe2[1]["y"]},
        ]

        pipe_vel_x = -4
        player_vel_y = -9
        player_max_vel_y = 10
        player_acc_y = 1
        player_flap_acc = -8
        player_flapped = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    return False
                if event.type == KEYDOWN and event.key in (K_SPACE, K_UP):
                    if player_y > 0:
                        player_vel_y = player_flap_acc
                        player_flapped = True
                        sounds["wing"].play()

            # ── Collision check ──
            if _is_collide(player_x, player_y, upper_pipes, lower_pipes, sprites, sounds):
                return True  # round over — return to welcome screen

            # ── Score check ──
            player_mid = player_x + sprites["player"].get_width() / 2
            for pipe in upper_pipes:
                pipe_mid = pipe["x"] + sprites["pipe"][0].get_width() / 2
                if pipe_mid <= player_mid < pipe_mid + 4:
                    score += 1
                    sounds["point"].play()

            # ── Physics ──
            if player_vel_y < player_max_vel_y and not player_flapped:
                player_vel_y += player_acc_y
            if player_flapped:
                player_flapped = False

            player_height = sprites["player"].get_height()
            player_y += min(player_vel_y, int(GROUND_Y) - player_y - player_height)

            # ── Move pipes ──
            for up, lp in zip(upper_pipes, lower_pipes):
                up["x"] += pipe_vel_x
                lp["x"] += pipe_vel_x

            # ── Spawn new pipes ──
            if 0 < upper_pipes[0]["x"] < 5:
                new = _get_random_pipe(sprites)
                upper_pipes.append(new[0])
                lower_pipes.append(new[1])

            # ── Remove off-screen pipes ──
            if upper_pipes[0]["x"] < -sprites["pipe"][0].get_width():
                upper_pipes.pop(0)
                lower_pipes.pop(0)

            # ── Draw everything ──
            screen.blit(sprites["background"], (0, 0))
            for up, lp in zip(upper_pipes, lower_pipes):
                screen.blit(sprites["pipe"][0], (up["x"], up["y"]))
                screen.blit(sprites["pipe"][1], (lp["x"], lp["y"]))

            screen.blit(sprites["base"], (0, GROUND_Y))
            screen.blit(sprites["player"], (player_x, player_y))

            # ── Draw score digits ──
            digits = [int(d) for d in str(score)]
            total_w = sum(sprites["numbers"][d].get_width() for d in digits)
            x_offset = (SCREEN_WIDTH - total_w) / 2
            for d in digits:
                screen.blit(sprites["numbers"][d], (x_offset, SCREEN_HEIGHT * 0.12))
                x_offset += sprites["numbers"][d].get_width()

            pygame.display.update()
            clock.tick(FPS)


# ── Module-level helpers (stateless) ──────────────────────────────────────────

def _get_random_pipe(sprites: dict) -> list[dict]:
    """Return a pair of dicts [upper, lower] with random y-positions."""
    pipe_height = sprites["pipe"][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2 = offset + random.randrange(
        0, int(SCREEN_HEIGHT - sprites["base"].get_height() - 1.2 * offset)
    )
    pipe_x = SCREEN_WIDTH + 10
    y1 = pipe_height - y2 + offset
    return [
        {"x": pipe_x, "y": -y1},  # upper pipe
        {"x": pipe_x, "y": y2},   # lower pipe
    ]


def _is_collide(
    player_x: int,
    player_y: int,
    upper_pipes: list[dict],
    lower_pipes: list[dict],
    sprites: dict,
    sounds: dict,
) -> bool:
    """Return True if the bird has crashed."""
    if player_y > GROUND_Y - 25 or player_y < 0:
        sounds["hit"].play()
        return True

    for pipe in upper_pipes:
        pipe_h = sprites["pipe"][0].get_height()
        if (
            player_y < pipe_h + pipe["y"]
            and abs(player_x - pipe["x"]) < sprites["pipe"][0].get_width()
        ):
            sounds["hit"].play()
            return True

    for pipe in lower_pipes:
        if (
            player_y + sprites["player"].get_height() > pipe["y"]
            and abs(player_x - pipe["x"]) < sprites["pipe"][0].get_width()
        ):
            sounds["hit"].play()
            return True

    return False
