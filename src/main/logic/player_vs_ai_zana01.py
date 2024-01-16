import numpy as np
import random
import pygame
import sys
import os
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from design.winner_box import winnerBox

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (255, 255, 255)

class ConnectFour:
    def __init__(self, row, column):
        self.ROW_COUNT = row
        self.COLUMN_COUNT = column
        self.PLAYER = 0
        self.AI = 1
        self.EMPTY = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.WINDOW_LENGTH = 4
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        self.game_over = False
        self.turn = random.randint(self.PLAYER, self.AI)
        os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'
        pygame.init()
        self.myfont = pygame.font.SysFont("Helvetica", 75)

        self.SQUARESIZE = 0
        self.RADIUS = 0

        self.width = 0
        self.height = 0

        self.size = (0, 0)

        self.RADIUS = 0
        self.screen = pygame.display.set_mode(self.size)
        
        # Calculate SQUARESIZE and RADIUS after creating the screen
        self.SQUARESIZE, self.RADIUS = self.calculate_square_size(self.screen)
        
        # Update width and height based on COLUMN_COUNT, ROW_COUNT, and SQUARESIZE
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
        
        # Update the size variable
        self.size = (self.width, self.height)
        
        # Update the screen with the new size
        self.screen = pygame.display.set_mode(self.size)

        self.draw_board(self.board)
        pygame.display.update()
        self.myfont = pygame.font.SysFont("Helvetica", 75)

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[self.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        print(np.flip(board, 0))


    def winning_move(self, board, piece):


        horizontal, vertical, negative_diagonal_col, negative_diagonal_row, positive_diagonal_col, positive_diagonal_row = self.get_winning_position_based_on_table(self.ROW_COUNT, self.COLUMN_COUNT)

        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True


    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(self.COLUMN_COUNT-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(self.ROW_COUNT-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.AI_PIECE):
                    return (None, 100000000000000)
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, self.AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, board, piece):

        valid_locations = self.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):      
                if board[r][c] == self.PLAYER_PIECE:
                    pygame.draw.circle(self.screen, RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board[r][c] == self.AI_PIECE: 
                    pygame.draw.circle(self.screen, YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()


    def play_game(self):
        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0,0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == self.PLAYER:
                        pygame.draw.circle(self.screen, RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, BLACK, (0,0, self.width, self.SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                    if self.turn == self.PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, self.PLAYER_PIECE)

                            if self.winning_move(self.board, self.PLAYER_PIECE):
                                self.draw_board(self.board)
                                winnerBox("YOU WIN", self.refresh_function(), self.screen)
                                #label = self.myfont.render("Player 1 wins!!", 1, RED)
                                #self.screen.blit(label, (40,10))
                                self.game_over = True

                            self.turn += 1
                            self.turn = self.turn % 2

                            self.print_board(self.board)
                            self.draw_board(self.board)


            # # Ask for Player 2 Input
            if self.turn == self.AI and not self.game_over:                

                #col = random.randint(0, COLUMN_COUNT-1)
                #col = pick_best_move(board, AI_PIECE)
                col, minimax_score = self.minimax(self.board, 5, -math.inf, math.inf, True)

                if self.is_valid_location(self.board, col):
                    #pygame.time.wait(500)
                    row = self.get_next_open_row(self.board, col)
                    self.drop_piece(self.board, row, col, self.AI_PIECE)

                    if self.winning_move(self.board, self.AI_PIECE):
                        self.draw_board(self.board)
                        winnerBox("AI WINS", self.refresh_function(), self.screen)
                        #label = self.myfont.render("Player 2 wins!!", 1, YELLOW)
                        #self.screen.blit(label, (40,10))
                        self.game_over = True

                    self.print_board(self.board)
                    self.draw_board(self.board)

                    self.turn += 1
                    self.turn = self.turn % 2
 
            if self.is_draw(self.board):
                self.draw_board(self.board)
                winnerBox("ITS A DRAW", self.refresh_function(), self.screen)
                self.game_over = True 

            if self.game_over:
                pygame.time.wait(1000)

    def is_draw(self, board):
        i = 0
        for c in range(self.COLUMN_COUNT):
            if board[self.ROW_COUNT-1][c] != 0:
                i+=1
        return i == self.COLUMN_COUNT

    def calculate_square_size(self, screen):
        max_width = screen.get_width()
        max_height = screen.get_height()

        square_size_width = max_width // self.COLUMN_COUNT
        square_size_height = max_height // (self.ROW_COUNT + 1)

        # i percaktojna dimensionet sa me u kon ni square nqs tabela ma e vogel / madhe
        max_square_size_extrasmall = 90
        max_square_size_small = 78
        max_square_size_medium = 62
        max_square_size_smallmedium = 62
        max_square_size_large = 50

        if self.ROW_COUNT * self.COLUMN_COUNT <= 29:  # percaktojme madhesine e tabeles madhe/vogel
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_extrasmall)
        elif self.ROW_COUNT * self.COLUMN_COUNT <= 43:  # percaktojme madhesine e tabeles madhe/vogel
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_small)
        elif self.ROW_COUNT * self.COLUMN_COUNT <= 57:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_medium)
        elif self.ROW_COUNT * self.COLUMN_COUNT <= 65 and self.ROW_COUNT * self.COLUMN_COUNT != 63:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_smallmedium)
        else:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_large)

        RADIUS = int(SQUARESIZE / 2)
        
        return SQUARESIZE, RADIUS

    def refresh_function(self):
        print("Refresh function called")



    def get_winning_position_based_on_table(self, row, col):
        switch_dict = {
            #horizontal, vertical, negativ_col, negativ_row, positive_col, positive_row,
            (6, 7): (3, 3, 3, 3, 3, 3),
            (5, 4): (0, 1, 0, 1, 0, 1),

            # Add more cases as needed
        }

        # Default values in case the (row, col) pair is not in the dictionary
        default_values = (3, 3, 3, 3, 3, 3)

        # Use get method to retrieve values based on (row, col) pair
        horizontal, vertical, negative_diagonal_col, negative_diagonal_row, positive_diagonal_col, positive_diagonal_row = switch_dict.get((row, col), default_values)

        return horizontal, vertical, negative_diagonal_col, negative_diagonal_row, positive_diagonal_col, positive_diagonal_row

    # Example usage:


if __name__ == "__main__":
    game = ConnectFour(5, 4)
    game.play_game()


                