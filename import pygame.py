import pygame
import random

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 300, 600
BLOCK = 30
COLS = WIDTH // BLOCK
ROWS = HEIGHT // BLOCK

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

COLORS = [
    (0,255,255),
    (255,255,0),
    (128,0,128),
    (0,255,0),
    (255,0,0),
]

# 블록 모양
SHAPES = [
    [[1,1,1,1]],

    [[1,1],
     [1,1]],

    [[0,1,0],
     [1,1,1]],

    [[0,1,1],
     [1,1,0]],

    [[1,1,0],
     [0,1,1]],

    [[1,0],
     [1,0],
     [1,1]],

    [[0,1],
     [0,1],
     [1,1]],
]

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - 1
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

current_piece = Piece()

font = pygame.font.SysFont(None, 30)
score = 0

def draw_board():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x*BLOCK, y*BLOCK, BLOCK, BLOCK)

            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], rect)

            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (piece.x+x)*BLOCK,
                    (piece.y+y)*BLOCK,
                    BLOCK,
                    BLOCK
                )
                pygame.draw.rect(screen, piece.color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

def valid_move(piece, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + dx
                ny = piece.y + y + dy

                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False

                if ny >= 0 and board[ny][nx]:
                    return False

    return True

def merge_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                board[piece.y+y][piece.x+x] = piece.color

def clear_lines():
    global board, score

    new_board = [row for row in board if any(v == 0 for v in row)]

    cleared = ROWS - len(new_board)

    for _ in range(cleared):
        new_board.insert(0, [0 for _ in range(COLS)])

    board = new_board
    score += cleared * 100

running = True
fall_time = 0
fall_speed = 500

while running:
    dt = clock.tick(60)
    fall_time += dt

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if valid_move(current_piece, dx=-1):
                    current_piece.x -= 1

            elif event.key == pygame.K_RIGHT:
                if valid_move(current_piece, dx=1):
                    current_piece.x += 1

            elif event.key == pygame.K_DOWN:
                if valid_move(current_piece, dy=1):
                    current_piece.y += 1

            elif event.key == pygame.K_UP:
                old = current_piece.shape
                current_piece.rotate()

                if not valid_move(current_piece):
                    current_piece.shape = old

    if fall_time > fall_speed:
        fall_time = 0

        if valid_move(current_piece, dy=1):
            current_piece.y += 1
        else:
            merge_piece(current_piece)
            clear_lines()
            current_piece = Piece()

            if not valid_move(current_piece):
                running = False

    draw_board()
    draw_piece(current_piece)

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()