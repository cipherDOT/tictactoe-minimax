# todo:
#   [X] aesthetic improvements
#   [X] implement minimax
#   [ ] optimize code
#       - [ ] alpha beta pruning in minimax
#   [X] implement pretty print for results[x wins, o wins, tie...]

import pygame
import time
import math

pygame.font.init()

# display and visual variables
width = 600
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')


line_x = width // 3
line_y = height // 3
line_color = (0, 200, 150)
x_color = (250, 200, 150)
o_color = (150, 250, 200)

# ---------------------------------------------------------------------------------------------------------------- #
# section 2


class Tacboard(object):
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def draw_x(self, pos):
        x = pos[0]
        y = pos[1]
        if self.available((x, y)):
            pygame.draw.line(display, x_color, ((x * line_x) + (line_x // 4), (y * line_y) + (line_y // 4)),
                             ((x * line_x) + (3 * (line_x // 4)), (y * line_y) + (3 * (line_y // 4))), 2)
            pygame.draw.line(display, x_color, ((x * line_x) + (3 * (line_x // 4)), (y * line_y) +
                                                (line_y // 4)), ((x * line_x) + (line_x // 4), (y * line_y) + (3 * (line_y // 4))), 2)

            self.board[pos[0]][pos[1]] = 1

        else:
            print(f"Position [{x},{y}] already occupied")

    def draw_o(self, pos):
        x = pos[0]
        y = pos[1]
        if self.available((x, y)):
            pygame.draw.circle(display, o_color, (((x * line_x) + (line_x // 2)),
                                                  ((y * line_y) + (line_y // 2))), (3 * (line_x // 8)), 2)

            self.board[pos[0]][pos[1]] = -1

        else:
            print(f"Position [{x},{y}] already occupied")

    def available(self, pos):
        return self.board[pos[0]][pos[1]] == 0

    # gets the win/tie/ongoing state of the board
    def state(self):

        # return 1 or -1 if X or O wins respectively

        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[1][1] if self.board[1][1] != 0 else None

        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[1][1] if self.board[1][1] != 0 else None

        else:
            for i in range(3):
                if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                    return self.board[i][0] if self.board[i][0] != 0 else None

            for j in range(3):
                if self.board[0][j] == self.board[1][j] == self.board[2][j]:
                    return self.board[0][j] if self.board[0][j] != 0 else None

        # return a "TIE"
        if self.full():
            return 0

        return None

    # draws the graphical board
    def draw_board(self):
        # draws the layout of the board
        if width % 3 == 0:
            if height % 3 == 0:
                pygame.draw.line(display, line_color,
                                 (0, line_y), (width, line_y), 2)
                pygame.draw.line(display, line_color,
                                 (0, line_y * 2), (width, line_y * 2), 2)
                pygame.draw.line(display, line_color,
                                 (line_x, 0), (line_x, height), 2)
                pygame.draw.line(display, line_color,
                                 (line_x * 2, 0), (line_x * 2, height), 2)
                pygame.display.flip()

    # checks whether there are no available positions in the board
    def full(self):
        for i in self.board:
            for j in i:
                if j == 0:
                    return False

        return True

# --------------------------------------------minmax alogorithm----------------------------------------------------------- #

# this recursive function claculates ALL THE POSSIBLE moves that can be played
# at each point in the game and plays the most optimal move for itself
# by analyzing each point in the game


def minimax(board, depth, maxim):
    # checks if there is a winner and returns the winner score
    state = board.state()
    if state != None:
        return state

    # the maximizing player turn
    if maxim:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                # if a position is available it
                # makes a move there and sees the end results
                # and makes a score for each move. then it
                # plays the best possible move for X, i.e., the
                # highest score
                if board.available((i, j)):
                    board.board[i][j] = 1
                    score = minimax(board, depth + 1, False)
                    board.board[i][j] = 0
                    # maximizing the score
                    best_score = max(best_score, score)

        return best_score

    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                # if a position is available it
                # makes a move there and sees the end results
                # and makes a score for each move. then it
                # plays the best possible move for O, i.e., the
                # lowest score
                if board.available((i, j)):
                    board.board[i][j] = -1
                    score = minimax(board, depth + 1, True)
                    board.board[i][j] = 0
                    # minimizing the score
                    best_score = min(best_score, score)

        return best_score

# -------------------------------------mouse position function------------------------------------------------------ #


def get_mouse_pos():
    return (pygame.mouse.get_pos()[0] // line_x, pygame.mouse.get_pos()[1] // line_x)

# ---------------------------------------announce function---------------------------------------------------------- #

# pretty prints the winner or the TIE state


def announce(player):
    print('')
    if player == 'TIE':
        print('TIE')
    else:
        print(f'{player} wins!')
    print('')

# -------------------------------------------main loop------------------------------------------------------------ #

# section 4
# main game loop of the program


def main():
    run = True
    turn = 0
    click = 0
    board = Tacboard()
    end_state = False

    while run:
        board.draw_board()
        if end_state:
            time.sleep(2)
            run = False
            quit()

        # checks if it's the AI's turn and plays accordingly.
        # here the ai is the maximizing player (X player).
        if turn % 2 == 0:
            best_score = -math.inf
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board.available((i, j)):
                        board.board[i][j] = 1
                        # the next turn is the minimizing players turn
                        # and hence the boolean "maxim" is set to false
                        score = minimax(board, 0, False)
                        board.board[i][j] = 0
                        if score > best_score:
                            # the best score and the best move are
                            # recorded to play the best move
                            best_score = score
                            best_move = (i, j)

            board.draw_x(best_move)
            turn += 1

        # ------------event handler---------------------- #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click += 1
                pos = get_mouse_pos()
                if turn % 2 == 1:
                    board.draw_o(pos)

                if click >= 12:
                    run = False

                turn += 1

        # ----- state analysis for each frame ----- #

        state = board.state()

        if state == 1:
            announce('X')
            end_state = True
        elif state == -1:
            announce('O')
            end_state = True
        elif state == 0:
            announce('TIE')
            end_state = True
        else:
            pass

        # ----------------------------------------- #

        pygame.display.flip()

# ---------------------------------------------------------------------------------------------------------------- #


# initiating the game loop
if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------------------------------------------- #
