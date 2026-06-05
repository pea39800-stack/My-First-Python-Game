import pygame
import random

pygame.init()

pygame.key.set_repeat(200, 80)

BLOCK = 30
COLS = 10
ROWS = 20

PLAY_WIDTH = COLS * BLOCK
PLAY_HEIGHT = ROWS * BLOCK

SIDE_PANEL = 150

WIDTH = PLAY_WIDTH + SIDE_PANEL
HEIGHT = PLAY_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)

CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 100, 255)

ALL_COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]

PIECES = [
    (
        [[1, 1, 1, 1]],
        CYAN
    ),
    (
        [[1, 1],
         [1, 1]],
        YELLOW
    ),
    (
        [[0, 1, 0],
         [1, 1, 1]],
        PURPLE
    ),
    (
        [[0, 1, 1],
         [1, 1, 0]],
        GREEN
    ),
    (
        [[1, 1, 0],
         [0, 1, 1]],
        RED
    ),
    (
        [[1, 0],
         [1, 0],
         [1, 1]],
        ORANGE
    ),
    (
        [[0, 1],
         [0, 1],
         [1, 1]],
        BLUE
    )
]

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 60)

score = 0
lines_cleared = 0


class Piece:
    def __init__(self):
        shape, _ = random.choice(PIECES)

        self.shape = [row[:] for row in shape]
        self.color = random.choice(ALL_COLORS)

        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


current_piece = Piece()
next_piece = Piece()

def valid_move(piece, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if not cell:
                continue

            nx = piece.x + x + dx
            ny = piece.y + y + dy

            if nx < 0 or nx >= COLS:
                return False

            if ny >= ROWS:
                return False

            if ny >= 0 and board[ny][nx]:
                return False

    return True


def merge_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                by = piece.y + y
                bx = piece.x + x

                if 0 <= by < ROWS:
                    board[by][bx] = piece.color


def clear_lines():
    global board, score, lines_cleared

    new_board = [row for row in board if any(cell == 0 for cell in row)]

    removed = ROWS - len(new_board)

    for _ in range(removed):
        new_board.insert(0, [0] * COLS)

    board = new_board

    if removed:
        lines_cleared += removed
        score += removed * 100


def draw_board():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(
                x * BLOCK,
                y * BLOCK,
                BLOCK,
                BLOCK
            )

            if board[y][x]:
                pygame.draw.rect(
                    screen,
                    board[y][x],
                    rect
                )

            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (piece.x + x) * BLOCK,
                    (piece.y + y) * BLOCK,
                    BLOCK,
                    BLOCK
                )

                pygame.draw.rect(
                    screen,
                    piece.color,
                    rect
                )

                pygame.draw.rect(
                    screen,
                    WHITE,
                    rect,
                    1
                )


def draw_ghost(piece):
    ghost_y = piece.y

    while True:
        test_piece = Piece()
        test_piece.shape = piece.shape
        test_piece.color = piece.color
        test_piece.x = piece.x
        test_piece.y = ghost_y + 1

        if valid_move(test_piece):
            ghost_y += 1
        else:
            break

    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (piece.x + x) * BLOCK,
                    (ghost_y + y) * BLOCK,
                    BLOCK,
                    BLOCK
                )

                pygame.draw.rect(
                    screen,
                    (80, 80, 80),
                    rect,
                    2
                )


def draw_side_panel():
    panel_x = PLAY_WIDTH + 10

    title = font.render("NEXT", True, WHITE)
    screen.blit(title, (panel_x, 20))

    for y, row in enumerate(next_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    panel_x + x * BLOCK,
                    60 + y * BLOCK,
                    BLOCK,
                    BLOCK
                )

                pygame.draw.rect(
                    screen,
                    next_piece.color,
                    rect
                )

                pygame.draw.rect(
                    screen,
                    WHITE,
                    rect,
                    1
                )

    screen.blit(
        font.render(f"Score", True, WHITE),
        (panel_x, 180)
    )

    screen.blit(
        font.render(str(score), True, WHITE),
        (panel_x, 210)
    )

    level = lines_cleared // 10 + 1

    screen.blit(
        font.render(f"Level", True, WHITE),
        (panel_x, 280)
    )

    screen.blit(
        font.render(str(level), True, WHITE),
        (panel_x, 310)
    )


running = True
game_over = False

fall_timer = 0

while running:

    dt = clock.tick(60)
    fall_timer += dt

    level = lines_cleared // 10 + 1
    fall_speed = max(100, 600 - (level - 1) * 40)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_over:
            continue

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if valid_move(current_piece, dx=-1):
                    current_piece.x -= 1

            elif event.key == pygame.K_RIGHT:
                if valid_move(current_piece, dx=1):
                    current_piece.x += 1

            elif event.key == pygame.K_DOWN:
                if valid_move(current_piece, dy=1):
                    current_piece.y += 1

            elif event.key == pygame.K_SPACE:
                while valid_move(current_piece, dy=1):
                    current_piece.y += 1

            elif event.key == pygame.K_UP:

                old_shape = [row[:] for row in current_piece.shape]

                current_piece.rotate()

                if not valid_move(current_piece):
                    current_piece.shape = old_shape

    if not game_over and fall_timer >= fall_speed:

        fall_timer = 0

        if valid_move(current_piece, dy=1):
            current_piece.y += 1

        else:
            merge_piece(current_piece)
            clear_lines()

            current_piece = next_piece
            next_piece = Piece()

            if not valid_move(current_piece):
                game_over = True

    screen.fill(BLACK)

    draw_board()

    if not game_over:
        draw_ghost(current_piece)
        draw_piece(current_piece)

    draw_side_panel()

    if game_over:
        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            text,
            (
                PLAY_WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - 30
            )
        )

    pygame.display.flip()

pygame.quit()