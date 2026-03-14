"""
Snake Game — a pygame-based classic arcade game for Game Arcadia.

No external assets required — everything is drawn procedurally.
The game launches a separate pygame window and returns control to
the terminal menu when the player closes it or presses Escape.
"""

import random

try:
    import pygame
    from pygame.locals import (
        QUIT, KEYDOWN,
        K_ESCAPE, K_SPACE, K_RETURN,
        K_UP, K_DOWN, K_LEFT, K_RIGHT,
    )
except ImportError:
    pygame = None

from core.settings import Colors
from core.utils import clear_screen, pause
from game_arcadia.games.base_game import BaseGame

# ── Game constants ───────────────────────────────────────────────────────────
CELL_SIZE = 30
GRID_COLS = 20
GRID_ROWS = 20
SCREEN_WIDTH = CELL_SIZE * GRID_COLS   # 600
SCREEN_HEIGHT = CELL_SIZE * GRID_ROWS + 60  # 660 (extra 60px for HUD)
HUD_HEIGHT = 60
FPS = 10  # base speed

# ── Colour palette ───────────────────────────────────────────────────────────
COL_BG          = (18, 18, 30)
COL_GRID_LINE   = (28, 28, 45)
COL_SNAKE_HEAD  = (0, 200, 83)
COL_SNAKE_BODY  = (0, 230, 118)
COL_SNAKE_DARK  = (0, 150, 60)
COL_FOOD        = (255, 69, 58)
COL_FOOD_SHINE  = (255, 120, 110)
COL_TEXT         = (230, 230, 250)
COL_TEXT_DIM     = (130, 130, 160)
COL_HUD_BG      = (12, 12, 22)
COL_OVERLAY     = (0, 0, 0, 180)
COL_GOLD        = (255, 215, 0)
COL_ACCENT      = (100, 108, 255)

# ── Directions ───────────────────────────────────────────────────────────────
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class SnakeGame(BaseGame):
    """Classic Snake game wrapped in the BaseGame interface."""

    # ── BaseGame interface ────────────────────────────────────────────────
    def get_name(self) -> str:
        return "🐍 Snake"

    def get_description(self) -> str:
        return "Classic snake — eat, grow, don't crash!"

    def start(self) -> None:
        """Entry point called by the launcher."""
        if pygame is None:
            clear_screen()
            print(f"\n  {Colors.RED}{Colors.BOLD}⚠  pygame is not installed!{Colors.RESET}")
            print(f"  {Colors.DIM}Run:  pip install pygame{Colors.RESET}")
            pause()
            return

        try:
            self._run_game()
        except Exception as exc:
            pygame.quit()
            clear_screen()
            print(f"\n  {Colors.RED}{Colors.BOLD}⚠  Snake crashed:{Colors.RESET}")
            print(f"  {Colors.DIM}{exc}{Colors.RESET}")
            pause()

    # ── Private: full game lifecycle ──────────────────────────────────────
    def _run_game(self) -> None:
        """Initialise pygame and run the welcome → play → game-over loop."""
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake — GameHub")
        clock = pygame.time.Clock()

        try:
            while True:
                action = self._welcome_screen(screen, clock)
                if action == "quit":
                    break
                # Play rounds until the player chooses to quit
                while True:
                    result = self._play_round(screen, clock)
                    if result == "quit":
                        return
                    # result == "dead" → show game-over
                    action = self._game_over_screen(screen, clock, result)
                    if action == "quit":
                        return
                    if action == "menu":
                        break  # back to welcome
                    # action == "retry" → loop again
        finally:
            pygame.quit()

    # ── Welcome screen ────────────────────────────────────────────────────
    def _welcome_screen(self, screen, clock) -> str:
        """Animated title screen. Returns 'play' or 'quit'."""
        font_big = pygame.font.SysFont("Segoe UI", 52, bold=True)
        font_med = pygame.font.SysFont("Segoe UI", 22)
        font_sm  = pygame.font.SysFont("Segoe UI", 16)

        # Decorative background snake path
        demo_snake = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10)]
        demo_dir = RIGHT
        demo_timer = 0

        blink_timer = 0
        show_prompt = True

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return "quit"
                if event.type == KEYDOWN and event.key in (K_SPACE, K_RETURN):
                    return "play"

            # Animate demo snake
            demo_timer += 1
            if demo_timer % 6 == 0:
                demo_snake, demo_dir = _move_demo_snake(demo_snake, demo_dir)

            # Blink prompt
            blink_timer += 1
            if blink_timer % 20 == 0:
                show_prompt = not show_prompt

            # ── Draw ──
            screen.fill(COL_BG)
            _draw_grid(screen)

            # Draw demo snake
            for i, (cx, cy) in enumerate(demo_snake):
                color = COL_SNAKE_HEAD if i == 0 else COL_SNAKE_BODY
                rect = pygame.Rect(cx * CELL_SIZE, cy * CELL_SIZE + HUD_HEIGHT, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect.inflate(-4, -4), border_radius=6)

            # Title
            title_surf = font_big.render("SNAKE", True, COL_SNAKE_BODY)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(title_surf, title_rect)

            # Decorative line
            pygame.draw.line(screen, COL_ACCENT,
                             (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25),
                             (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 - 25), 2)

            # Subtitle
            sub_surf = font_med.render("Eat  ·  Grow  ·  Survive", True, COL_TEXT_DIM)
            sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5))
            screen.blit(sub_surf, sub_rect)

            # Prompt
            if show_prompt:
                prompt_surf = font_sm.render("Press SPACE to start", True, COL_GOLD)
                prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                screen.blit(prompt_surf, prompt_rect)

            # Controls hint
            hint = font_sm.render("Arrow keys to move  ·  ESC to quit", True, COL_TEXT_DIM)
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))

            pygame.display.update()
            clock.tick(FPS * 2)

    # ── Core gameplay round ───────────────────────────────────────────────
    def _play_round(self, screen, clock) -> str | int:
        """
        Run one round. Returns 'quit' or the final score (int) on death.
        """
        font_hud = pygame.font.SysFont("Segoe UI", 24, bold=True)
        font_hud_label = pygame.font.SysFont("Segoe UI", 14)

        # Initial snake: 3 segments, middle of the board, facing right
        snake = [(GRID_COLS // 2, GRID_ROWS // 2)]
        for i in range(1, 4):
            snake.append((GRID_COLS // 2 - i, GRID_ROWS // 2))

        direction = RIGHT
        next_direction = RIGHT
        score = 0
        food = _spawn_food(snake)
        speed = FPS

        # Animation accumulators
        food_pulse = 0

        while True:
            # ── Events ──
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return "quit"
                if event.type == KEYDOWN:
                    if event.key == K_UP and direction != DOWN:
                        next_direction = UP
                    elif event.key == K_DOWN and direction != UP:
                        next_direction = DOWN
                    elif event.key == K_LEFT and direction != RIGHT:
                        next_direction = LEFT
                    elif event.key == K_RIGHT and direction != LEFT:
                        next_direction = RIGHT

            direction = next_direction

            # ── Move snake ──
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Wall collision
            if not (0 <= new_head[0] < GRID_COLS and 0 <= new_head[1] < GRID_ROWS):
                return score

            # Self collision
            if new_head in snake:
                return score

            snake.insert(0, new_head)

            # ── Eat food? ──
            if new_head == food:
                score += 1
                food = _spawn_food(snake)
                # Speed up every 5 points, cap at 25
                speed = min(FPS + score // 5 * 2, 25)
            else:
                snake.pop()

            # ── Draw ──
            screen.fill(COL_BG)
            _draw_grid(screen)

            # Food (pulsing circle)
            food_pulse = (food_pulse + 1) % 30
            pulse_offset = abs(food_pulse - 15) / 15.0  # 0..1
            food_radius = int(CELL_SIZE * 0.38 + pulse_offset * 3)
            food_center = (
                food[0] * CELL_SIZE + CELL_SIZE // 2,
                food[1] * CELL_SIZE + HUD_HEIGHT + CELL_SIZE // 2,
            )
            # Glow
            pygame.draw.circle(screen, (80, 20, 20), food_center, food_radius + 5)
            pygame.draw.circle(screen, COL_FOOD, food_center, food_radius)
            # Shine
            shine_pos = (food_center[0] - food_radius // 3, food_center[1] - food_radius // 3)
            pygame.draw.circle(screen, COL_FOOD_SHINE, shine_pos, max(food_radius // 4, 2))

            # Snake body (draw tail → head so head is on top)
            for i in reversed(range(len(snake))):
                cx, cy = snake[i]
                rect = pygame.Rect(
                    cx * CELL_SIZE, cy * CELL_SIZE + HUD_HEIGHT,
                    CELL_SIZE, CELL_SIZE,
                )
                if i == 0:
                    # Head — darker, slightly larger feel
                    pygame.draw.rect(screen, COL_SNAKE_HEAD, rect.inflate(-2, -2), border_radius=8)
                    # Eyes
                    _draw_eyes(screen, rect, direction)
                else:
                    # Body gradient: brighter near head, darker at tail
                    t = i / max(len(snake) - 1, 1)
                    r = int(COL_SNAKE_BODY[0] * (1 - t * 0.4))
                    g = int(COL_SNAKE_BODY[1] * (1 - t * 0.3))
                    b = int(COL_SNAKE_BODY[2] * (1 - t * 0.4))
                    color = (r, g, b)
                    pygame.draw.rect(screen, color, rect.inflate(-4, -4), border_radius=6)
                    # Subtle inner highlight
                    pygame.draw.rect(screen, COL_SNAKE_DARK, rect.inflate(-4, -4), width=1, border_radius=6)

            # ── HUD ──
            pygame.draw.rect(screen, COL_HUD_BG, (0, 0, SCREEN_WIDTH, HUD_HEIGHT))
            pygame.draw.line(screen, COL_ACCENT, (0, HUD_HEIGHT - 1), (SCREEN_WIDTH, HUD_HEIGHT - 1), 2)

            # Score
            score_label = font_hud_label.render("SCORE", True, COL_TEXT_DIM)
            screen.blit(score_label, (20, 8))
            score_val = font_hud.render(str(score), True, COL_GOLD)
            screen.blit(score_val, (20, 28))

            # Length
            len_label = font_hud_label.render("LENGTH", True, COL_TEXT_DIM)
            screen.blit(len_label, (SCREEN_WIDTH - 90, 8))
            len_val = font_hud.render(str(len(snake)), True, COL_TEXT)
            screen.blit(len_val, (SCREEN_WIDTH - 90, 28))

            # Game title
            title_surf = font_hud_label.render("SNAKE  ·  GameHub", True, COL_ACCENT)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, HUD_HEIGHT // 2))
            screen.blit(title_surf, title_rect)

            pygame.display.update()
            clock.tick(speed)

    # ── Game-over screen ──────────────────────────────────────────────────
    def _game_over_screen(self, screen, clock, final_score: int) -> str:
        """
        Show game-over overlay. Returns 'retry', 'menu', or 'quit'.
        """
        font_big = pygame.font.SysFont("Segoe UI", 48, bold=True)
        font_med = pygame.font.SysFont("Segoe UI", 26)
        font_sm  = pygame.font.SysFont("Segoe UI", 18)

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COL_OVERLAY)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return "quit"
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_RETURN:
                        return "retry"
                    if event.key in (K_LEFT, K_RIGHT):  # back to menu
                        return "menu"

            screen.blit(overlay, (0, 0))

            # Panel
            panel_w, panel_h = 340, 260
            panel_x = (SCREEN_WIDTH - panel_w) // 2
            panel_y = (SCREEN_HEIGHT - panel_h) // 2
            panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
            pygame.draw.rect(screen, (20, 20, 35), panel_rect, border_radius=16)
            pygame.draw.rect(screen, COL_ACCENT, panel_rect, width=2, border_radius=16)

            # "GAME OVER"
            go_surf = font_big.render("GAME OVER", True, COL_FOOD)
            go_rect = go_surf.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 55))
            screen.blit(go_surf, go_rect)

            # Score
            score_surf = font_med.render(f"Score: {final_score}", True, COL_GOLD)
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 115))
            screen.blit(score_surf, score_rect)

            # Divider
            pygame.draw.line(screen, COL_ACCENT,
                             (panel_x + 40, panel_y + 150),
                             (panel_x + panel_w - 40, panel_y + 150), 1)

            # Options
            opt1 = font_sm.render("SPACE  →  Play Again", True, COL_TEXT)
            screen.blit(opt1, opt1.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 185)))

            opt2 = font_sm.render("← / →  →  Back to Menu", True, COL_TEXT_DIM)
            screen.blit(opt2, opt2.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 215)))

            opt3 = font_sm.render("ESC  →  Quit", True, COL_TEXT_DIM)
            screen.blit(opt3, opt3.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 240)))

            pygame.display.update()
            clock.tick(FPS)


# ── Module-level helpers ──────────────────────────────────────────────────────

def _spawn_food(snake: list[tuple[int, int]]) -> tuple[int, int]:
    """Return a random grid cell not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1))
        if pos not in snake:
            return pos


def _draw_grid(screen) -> None:
    """Draw subtle grid lines on the play area."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, COL_GRID_LINE, (x, HUD_HEIGHT), (x, SCREEN_HEIGHT))
    for y in range(HUD_HEIGHT, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, COL_GRID_LINE, (0, y), (SCREEN_WIDTH, y))


def _draw_eyes(screen, head_rect: pygame.Rect, direction: tuple[int, int]) -> None:
    """Draw two small white eyes on the snake head, offset by direction."""
    cx, cy = head_rect.centerx, head_rect.centery
    eye_size = 4
    pupil_size = 2

    # Offset eyes perpendicular to direction, shift pupils in direction
    if direction in (UP, DOWN):
        offsets = [(-6, 0), (6, 0)]
        pupil_shift = (0, direction[1] * 3)
    else:
        offsets = [(0, -6), (0, 6)]
        pupil_shift = (direction[0] * 3, 0)

    for ox, oy in offsets:
        eye_pos = (cx + ox, cy + oy)
        pygame.draw.circle(screen, (255, 255, 255), eye_pos, eye_size)
        pupil_pos = (eye_pos[0] + pupil_shift[0], eye_pos[1] + pupil_shift[1])
        pygame.draw.circle(screen, (0, 0, 0), pupil_pos, pupil_size)


def _move_demo_snake(snake: list, direction: tuple) -> tuple[list, tuple]:
    """Move a demo snake randomly, staying in bounds. Returns (new_snake, new_dir)."""
    head_x, head_y = snake[0]

    # Occasionally change direction
    if random.random() < 0.25:
        choices = [UP, DOWN, LEFT, RIGHT]
        choices = [d for d in choices if d != OPPOSITE.get(direction, direction)]
        direction = random.choice(choices)

    new_head = (head_x + direction[0], head_y + direction[1])

    # Bounce off walls
    if not (0 <= new_head[0] < GRID_COLS and 0 <= new_head[1] < GRID_ROWS):
        # Try turning
        for d in [UP, DOWN, LEFT, RIGHT]:
            if d == OPPOSITE.get(direction):
                continue
            candidate = (head_x + d[0], head_y + d[1])
            if 0 <= candidate[0] < GRID_COLS and 0 <= candidate[1] < GRID_ROWS:
                direction = d
                new_head = candidate
                break
        else:
            # Fallback: reverse
            direction = OPPOSITE.get(direction, RIGHT)
            new_head = (head_x + direction[0], head_y + direction[1])

    new_snake = [new_head] + snake[:-1]
    return new_snake, direction
