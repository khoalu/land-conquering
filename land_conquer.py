import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,32)

import random

import pygame

pygame.init()
WIDTH = 1366
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH,HEIGHT))

background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
background = background.convert()

screen.blit(background, (0,0))

clock = pygame.time.Clock()


mainloop = True
FPS = 60           
playtime = 0.0

C_WHITE = (255,255,255)
C_BLACK = (0,0,0)
C_BLUE = (0, 140, 255)
C_DARKBLUE = (0, 0, 255)
C_RED = (255, 55, 55)
C_DARKRED = (255, 0 ,0)
C_GRAY = (200,200,200,128)
C_LIGHTGRAY = (211, 211, 211)
C_NEUTRAL = (180, 200, 255)

team1_name = "Construction"
team2_name = "ậ ẩ ẫ ă ắ ằ ẳ ẵ ặ ô ố"

font_name = "calibri"

font = pygame.font.SysFont(font_name, 50)
img1 = font.render('Turn: 2000', True, (80, 180, 255))
img2 = font.render(team1_name, True, C_BLUE)
img3 = font.render(team2_name, True, C_RED)

font_scores = pygame.font.SysFont(font_name, 72, 'bold')
img_score_1 = font_scores.render('20', True, C_BLUE)
img_score_2 = font_scores.render('40', True, C_RED)

def get_board(n_rows, n_cols):
    board = [[0 for j in range(n_cols)] for i in range(n_rows)]
    for i in range(n_rows):
        for j in range(n_cols):
            board[i][j] = random.randint(0, 2)

    return board


def draw_board(board, last_blue_coord, last_red_coord):
    top, left = 10, 10
    n_rows = len(board)
    n_cols = len(board[0])
    cell_size = (HEIGHT-10) // n_rows
    print("cell_size = ", cell_size)
    # board back ground : black

    pygame.draw.rect(screen, C_LIGHTGRAY, (top-2, left-2, n_cols * cell_size + 4, n_rows * cell_size + 4))

    for i in range(n_rows):
        for j in range(n_cols):
            cell_color = [C_GRAY, C_BLUE, C_RED][board[i][j]]
            pygame.draw.rect(screen, cell_color, (top + j * cell_size+1, left + i * cell_size+1, cell_size-2, cell_size-2))

    row, col = last_blue_coord
    pygame.draw.rect(screen, C_BLACK, (top + col * cell_size, left + row * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, C_DARKBLUE, (top + col * cell_size + 1, left + row * cell_size+1, cell_size-2, cell_size-2))

    row, col = last_red_coord
    pygame.draw.rect(screen, C_BLACK, (top + col * cell_size, left + row * cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, C_DARKRED, (top + col * cell_size + 1, left + row * cell_size+1, cell_size-2, cell_size-2))
        

def draw_scores():
    right = 550
    screen.blit(img1, (WIDTH-right, 20))

    screen.blit(img2, (WIDTH-right, 100))
    screen.blit(img_score_1, (WIDTH-right, 175))

    screen.blit(img3, (WIDTH-right, 300))
    screen.blit(img_score_2, (WIDTH-right, 375))

M = 20
N = 20
the_board = get_board(M, N)
last_blue = None
last_red = None
for i in range(M):
    for j in range(N):
        if the_board[i][j] == 1:
            last_blue = (i,j)
        elif the_board[i][j] == 2:
            last_red = (i,j)

while mainloop:
    miliseconds = clock.tick(FPS)
    playtime += miliseconds / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False

    text = "FPS: {0:2f}   Playtime: {1:2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    draw_board(the_board, last_blue, last_red)
    draw_scores()


    pygame.display.flip()

pygame.quit()
print("This game was played for {0:.2f} seconds".format(playtime))

