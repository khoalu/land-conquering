import subprocess, os
import time
import random
import pygame
from threading import Timer

class SetCommand(object):
    def __init__(self, player_id, row, col):
        self.player_id = player_id
        self.row = row
        self.col = col

class MoveCommand(object):
    def __init__(self, player_id, old_row, old_col, new_row, new_col):
        self.player_id = player_id
        self.old_row = old_row
        self.old_col = old_col
        self.new_row = new_row
        self.new_col = new_col

class Game(object):

    data_path = './data'

    C_WHITE = (255,255,255)
    C_BLACK = (0,0,0)
    C_BLUE = (0, 140, 255)
    C_DARKBLUE = (0, 0, 255)
    C_RED = (255, 100, 100)
    C_DARKRED = (255, 0 ,0)
    C_GRAY = (200,200,200,128)
    C_LIGHTGRAY = (211, 211, 211)
    C_NEUTRAL = (180, 200, 255)

    def __init__(self, N):
        self.N = N
        self.turn = 0
        self.MAX_TURN = 1000
        self.board = [[0 for i in range(N)] for j in range(N)]
        self.time_limit_per_turn = 5.0
        self.full_board = False
        self.command_queue = []
        self.game_end = False

        self.last_coord = [(-1,-1), (-1,-1)]

        # pygame
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,32)
        pygame.init()

        self.FPS = 60 # sua cai nay de chay nhanh / cham chuong trinh, o day fps = ups (update per second)

        self.WIDTH = 1366
        self.HEIGHT = 768
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255,255,255))
        self.background = self.background.convert()
        self.screen.blit(self.background, (0,0))
        self.clock = pygame.time.Clock()
        self.running = True

        self.team1_name = "Construction"
        self.team2_name = "ậ ẩ ẫ ă ắ ằ ẳ ẵ ặ ô ố"

        self.font_name = "calibri"
        self.font = pygame.font.SysFont(self.font_name, 50)
        
        self.img1 = self.font.render(self.team1_name, True, self.C_DARKBLUE)
        self.img2 = self.font.render(self.team2_name, True, self.C_DARKRED)

        self.font_scores = pygame.font.SysFont(self.font_name, 72, 'bold')

        

    def run(self):
        self.board[0][0] = 1
        self.board[self.N-1][self.N-1] = 2

        clock = self.clock
        
        self.draw()

        playtime = 0
        while self.running:
            miliseconds = clock.tick(self.FPS)
            playtime += miliseconds / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            text = "FPS: {0:2f}   Playtime: {1:2f}".format(clock.get_fps(), playtime)
            pygame.display.set_caption(text)

            if not self.game_end:
                self.update()
                self.draw()

            pygame.display.flip()            

    def update(self):
        self.turn += 1

        if self.check_full_board():
            print("END")
            self.display_board()
            self.game_end = True
                
        for player_id in range(1,3):
            # check if board is full
            if self.check_full_board():
                print("END")
                self.display_board()
                self.game_end = True
                break

            
            # delay at the start of player's turn
            ### NOTE: bo comment dong duoi de chuong trinh co delay trc khi thi sinh chay code (de ham random ko tra ve 1 gia tri lien tuc)
            # time.sleep(0.2)

            # distrubute board to player_id
            full_path = self.data_path + "/player_{}/".format(player_id)

            with open(full_path+"GAME.INP","w") as f:
                f.write(str(player_id)+'\n')
                f.write(str(self.turn+1)+'\n')
                f.write(str(self.N)+'\n')
                f.write(self.board_to_string())

            # execute player_id 's turn
            os.chdir(full_path) # to './data/player_{id}/'
            self.start_process(full_path)

            # read output from player_id and delete the file
            output = None
            if os.path.isfile("GAME.OUT"):
                f = open("GAME.OUT","r")
                output = f.readline()
                f.close()
                os.remove("GAME.OUT")
                print("got output of player {} = {}".format(player_id, output))
            else:
                print("No output file from player {}".format(player_id))
            
            os.chdir('../..') # to './'

            # update board
            if output is not None:
                self.update_board(output, player_id)
                # self.display_board()

    def draw(self):
        self.screen.blit(self.background, (0, 0)) # clear screen
        self.draw_board()
        self.draw_scores()

    def draw_scores(self):
        WIDTH = self.WIDTH

        img_turn = self.font.render('Turn: {}'.format(self.turn), True, (80, 180, 255))
        img_score_1 = self.font_scores.render(str(self.calc_score(1)), True, self.C_DARKBLUE)
        img_score_2 = self.font_scores.render(str(self.calc_score(2)), True, self.C_DARKRED)

        right = 550
        self.screen.blit(img_turn, (WIDTH-right, 20))

        self.screen.blit(self.img1, (WIDTH-right, 100))
        self.screen.blit(img_score_1, (WIDTH-right, 175))

        self.screen.blit(self.img2, (WIDTH-right, 300))
        self.screen.blit(img_score_2, (WIDTH-right, 375))

    def draw_board(self):
        board = self.board
        screen = self.screen
        HEIGHT = self.HEIGHT

        top, left = 10, 10
        n_rows = len(board)
        n_cols = len(board[0])
        cell_size = (HEIGHT-10) // n_rows
        # print("cell_size = ", cell_size)

        pygame.draw.rect(screen, self.C_LIGHTGRAY, (top-2, left-2, n_cols * cell_size + 4, n_rows * cell_size + 4))

        for i in range(n_rows):
            for j in range(n_cols):
                cell_color = [self.C_GRAY, self.C_BLUE, self.C_RED][board[i][j]]
                pygame.draw.rect(screen, cell_color, (top + j * cell_size+1, left + i * cell_size+1, cell_size-2, cell_size-2))

        last_blue_coord = self.last_coord[0]
        last_red_coord = self.last_coord[1]

        row, col = last_blue_coord
        if row != -1 and col != -1:
            pygame.draw.rect(screen, self.C_BLACK, (top + col * cell_size, left + row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, self.C_DARKBLUE, (top + col * cell_size + 1, left + row * cell_size+1, cell_size-2, cell_size-2))

        row, col = last_red_coord
        if row != -1 and col != -1:
            pygame.draw.rect(screen, self.C_BLACK, (top + col * cell_size, left + row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, self.C_DARKRED, (top + col * cell_size + 1, left + row * cell_size+1, cell_size-2, cell_size-2))


    def calc_score(self, player_id):
        N = self.N
        board = self.board

        score = 0
        for i in range(N):
            for j in range(N):
                if board[i][j] == player_id:
                    score += 1
        return score

    def check_full_board(self):
        N = self.N
        board = self.board
        for i in range(N):
            for j in range(N):
                if board[i][j] == 0:
                    return False
        return True

    def check_neighbor(self, r, c, player_id):
        td = [0, 1, 0, -1]
        tc = [1, 0, -1, 0]
        board = self.board
        for k in range(4):
            vr = r + td[k] 
            vc = c + tc[k]
            if self.inside_board(vr, vc) and board[vr][vc] == player_id:
                return True
        return False

    def inside_board(self, row, col):
        return row >= 0 and row < self.N and col >= 0 and col < self.N

    def update_board(self, command, player_id):
        tokens = command.split(' ')
        command_name = tokens[0].upper()

        board = self.board
        if command_name == 'SET':
            try:
                r = int(tokens[1]) - 1
                c = int(tokens[2]) - 1

                if not self.inside_board(r, c):
                    print('{} {} is not inside the board with size {}'.format(r, c, self.N))
                elif not self.check_neighbor(r, c, player_id):
                    print('no cell in 4 neighbors has the same color')
                elif board[r][c] != 0:
                    print('cell ({}, {}) is already occupied by player {}'.format(r, c, board[r][c]))
                else:
                    print('sucess placing ({}, {})'.format(r, c))
                    board[r][c] = player_id
                    self.last_coord[player_id-1] = (r, c)
                    

            except ValueError:
                print('Error in SET: some value in arguments is not an integer')
                print('tokens: ', tokens)
            except IndexError:
                print('Error in SET: not enough tokens')
                print('tokens: ', tokens)
                print('player_id: ', player_id)


        elif command_name == 'MOVE':
            try:
                old_r = int(tokens[1]) - 1
                old_c = int(tokens[2]) - 1
                new_r = int(tokens[3]) - 1
                new_c = int(tokens[4]) - 1

                if not self.inside_board(old_r, old_c):
                    print('old cell: {} {} is not inside the board with size {}'.format(old_r, old_c, self.N))
                elif not self.inside_board(new_r, new_c):
                    print('new cell: {} {} is not inside the board with size {}'.format(new_r, new_c, self.N))
                elif board[new_r][new_c] != 0:
                    print('new cell ({}, {}) is already occupied by player {}'.format(new_r, new_c, board[new_r][new_c]))
                elif board[old_r][old_c] == 0:
                    print('old cell ({}, {}) is empty'.format(old_r, old_c))
                else:
                    print('sucess moving ({}, {}) to ({}, {})'.format(old_r, old_c, new_r, new_c))
                    board[old_r][old_c] = 0
                    board[new_r][new_c] = player_id
                    self.last_coord[player_id-1] = (new_r, new_c)
                

            except ValueError:
                print('Error in MOVE: some value in arguments is not an integer')
                print('tokens: ', tokens)
            except IndexError:
                print('Error in SET: not enough tokens')
                print('tokens: ', tokens)
        else:
            print("Does not realize command name: ", command_name)
        
    def start_process(self, path):
        # kill the process if it run past the time limit
        t = Timer(self.time_limit_per_turn, lambda: subprocess.run("taskkill /f /im game.exe",shell=False))
        t.start()
        subprocess.run("GAME.exe",shell=False)
        t.cancel()

    def board_to_string(self):
        N = self.N
        board = self.board
        lines = ""
        for i in range(N):
            for j in range(N):
                lines += chr(board[i][j]+48)
            lines +='\n'
        return lines

    def display_board(self):
        N = self.N
        board = self.board
        for i in range(N):
            for j in range(N):
                print(board[i][j], end="")
            print()


def main():
    game = Game(20)
    game.run()


if __name__ == "__main__":
    main()