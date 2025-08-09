import pygame
import sys
import itertools

pygame.init()

WIDTH, HEIGHT = 300, 300
BOARD_ROWS, BOARD_COLS = 3, 3
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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
x_moves = []  # Keeps track of (row, col) for X's last 3 moves
o_moves = []  # Keeps track of (row, col) for O's last 3 moves

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*SQUARE_SIZE), (WIDTH, 2*SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*SQUARE_SIZE, 0), (2*SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    # Only display the 3 most recent moves for each player
    for idx, (row, col) in enumerate(x_moves):
        # Fade only the oldest if there are 3 moves
        color = FADED_COLOR if len(x_moves) == 3 and idx == 0 else CROSS_COLOR
        pygame.draw.line(screen, color,
                         (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                         (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                         CROSS_WIDTH)
        pygame.draw.line(screen, color,
                         (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                         (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                         CROSS_WIDTH)
    for idx, (row, col) in enumerate(o_moves):
        color = FADED_COLOR if len(o_moves) == 3 and idx == 0 else CIRCLE_COLOR
        pygame.draw.circle(screen, color,
                           (int(col * SQUARE_SIZE + SQUARE_SIZE//2),
                            int(row * SQUARE_SIZE + SQUARE_SIZE//2)),
                           CIRCLE_RADIUS, CIRCLE_WIDTH)

def available_square(row, col):
    # A square is available if it is not in the 3 latest X or O moves
    return (row, col) not in x_moves and (row, col) not in o_moves

def add_move(row, col, player):
    moves = x_moves if player == "X" else o_moves
    moves.append((row, col))
    # If more than 3 moves, remove the oldest and erase from board
    if len(moves) > 3:
        moves.pop(0)

def check_win(player):
    moves = x_moves if player == "X" else o_moves
    if len(moves) < 3:
        return False
    # Check every combination of 3 moves
    for combo in itertools.combinations(moves, 3):
        coords = set(combo)
        for row in range(BOARD_ROWS):
            if coords == set((row, col) for col in range(BOARD_COLS)):
                draw_horizontal_winning_line(row, player)
                return True
        for col in range(BOARD_COLS):
            if coords == set((row, col) for row in range(BOARD_ROWS)):
                draw_vertical_winning_line(col, player)
                return True
        if coords == set((i, i) for i in range(BOARD_ROWS)):
            draw_diagonal1(player)
            return True
        if coords == set((i, BOARD_ROWS - 1 - i) for i in range(BOARD_ROWS)):
            draw_diagonal2(player)
            return True
    return False


'''def check_win(player):
    moves = x_moves if player == "X" else o_moves
    if len(moves) < 3:
        return False
    coords = set(moves)
    for row in range(BOARD_ROWS):
        line = set((row, col) for col in range(BOARD_COLS))
        if line <= coords:
            draw_horizontal_winning_line(row, player)
            return True
    for col in range(BOARD_COLS):
        line = set((row, col) for row in range(BOARD_ROWS))
        if line <= coords:
            draw_vertical_winning_line(col, player)
            return True
    diag1 = set((i, i) for i in range(BOARD_ROWS))
    diag2 = set((i, BOARD_ROWS - 1 - i) for i in range(BOARD_ROWS))
    if diag1 <= coords:
        draw_diagonal1(player)
        return True
    if diag2 <= coords:
        draw_diagonal2(player)
        return True
    return False'''

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE//2
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (posX, 15), (posX, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE//2
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)

def draw_diagonal1(player):
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (15,15), (WIDTH-15, HEIGHT-15), WIN_LINE_WIDTH)

def draw_diagonal2(player):
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR,
                     (15, HEIGHT-15), (WIDTH-15, 15), WIN_LINE_WIDTH)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    x_moves.clear()
    o_moves.clear()

draw_lines()
player = "X"
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if available_square(clicked_row, clicked_col):
                add_move(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = "O" if player == "X" else "X"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = "X"
                game_over = False

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    pygame.display.update()
