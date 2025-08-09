import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 300, 300
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
LINE_WIDTH = 5
WIN_LINE_WIDTH = 5
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
FADED_COLOR = (180, 180, 180)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board state
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Move histories
x_moves = []  # List of (row, col) for X
o_moves = []  # List of (row, col) for O

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                # Faded if not latest
                color = FADED_COLOR if (row, col) in o_moves[:-1] and len(o_moves) == 3 else CIRCLE_COLOR
                pygame.draw.circle(screen, color,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                color = FADED_COLOR if (row, col) in x_moves[:-1] and len(x_moves) == 3 else CROSS_COLOR
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def add_move(row, col, player):
    if player == "X":
        x_moves.append((row, col))
        if len(x_moves) > 3:
            old_row, old_col = x_moves.pop(0)
            board[old_row][old_col] = None  # Remove oldest X
    else:
        o_moves.append((row, col))
        if len(o_moves) > 3:
            old_row, old_col = o_moves.pop(0)
            board[old_row][old_col] = None  # Remove oldest O

def is_board_full():
    # Only latest 3 for each player are "on" board
    active_cells = [cell for row in board for cell in row if cell is not None]
    return len(active_cells) >= 6

def check_win(player):
    moves = x_moves if player == "X" else o_moves
    if len(moves) < 3:
        return False
    # Check lines among current moves
    coords = set(moves)
    # Horizontal
    for row in range(BOARD_ROWS):
        line = set((row, col) for col in range(BOARD_COLS))
        if line <= coords:
            draw_horizontal_winning_line(row, player)
            return True
    # Vertical
    for col in range(BOARD_COLS):
        line = set((row, col) for row in range(BOARD_ROWS))
        if line <= coords:
            draw_vertical_winning_line(col, player)
            return True
    # Diagonals
    diag1 = set((i, i) for i in range(BOARD_ROWS))
    diag2 = set((i, BOARD_ROWS - 1 - i) for i in range(BOARD_ROWS))
    if diag1 <= coords:
        draw_diagonal1(player)
        return True
    if diag2 <= coords:
        draw_diagonal2(player)
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (posX, 15), (posX, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)

def draw_diagonal1(player):
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_diagonal2(player):
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None
    x_moves.clear()
    o_moves.clear()

# Setup
draw_lines()
player = "X"
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                add_move(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = "O" if player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = "X"
                game_over = False

    draw_figures()
    pygame.display.update()
