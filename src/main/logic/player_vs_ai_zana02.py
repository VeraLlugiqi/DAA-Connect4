import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import math

BLUE = "#0000FF"
RED = "#FF0000"
YELLOW = "#FFFF00"
BLACK = "#FFFFFF"

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

        self.root = tk.Tk()
        self.root.title("Connect Four")

        self.canvas = tk.Canvas(self.root, width=700, height=600)
        self.canvas.pack()

        self.SQUARESIZE, self.RADIUS = self.calculate_square_size()

        self.draw_board()

        self.root.after(100, self.play_game)
        self.root.mainloop()

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

    def draw_board(self):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                x0 = c * self.SQUARESIZE
                y0 = r * self.SQUARESIZE
                x1 = x0 + self.SQUARESIZE
                y1 = y0 + self.SQUARESIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=BLUE, outline=BLACK)
                self.canvas.create_oval(x0 + self.RADIUS, y1 - self.RADIUS, x1 - self.RADIUS, y0 + self.RADIUS, fill=BLACK, outline=BLACK)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == self.PLAYER_PIECE:
                    x = c * self.SQUARESIZE + self.SQUARESIZE // 2
                    y = self.ROW_COUNT * self.SQUARESIZE - r * self.SQUARESIZE - self.SQUARESIZE // 2
                    self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill=RED, outline=BLACK)
                elif self.board[r][c] == self.AI_PIECE:
                    x = c * self.SQUARESIZE + self.SQUARESIZE // 2
                    y = self.ROW_COUNT * self.SQUARESIZE - r * self.SQUARESIZE - self.SQUARESIZE // 2
                    self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill=YELLOW, outline=BLACK)

    def play_game(self):
        for event in self.root.event_generate("<<UpdateGame>>", when="tail"):
            if event.type == tk.EventType.KeyPress and event.keysym == "Escape":
                self.root.destroy()
                return

        if not self.game_over:
            if self.turn == self.PLAYER:
                self.root.bind("<Motion>", self.on_mouse_motion)
                self.root.bind("<Button-1>", self.on_mouse_click)
            elif self.turn == self.AI:
                self.root.after(500, self.ai_move)

    def on_mouse_motion(self, event):
        self.canvas.delete("cursor")
        posx = event.x
        if self.turn == self.PLAYER:
            x = posx // self.SQUARESIZE * self.SQUARESIZE + self.SQUARESIZE // 2
            y = self.SQUARESIZE // 2
            self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill=RED, outline=BLACK, tags="cursor")

    def on_mouse_click(self, event):
        posx = event.x
        col = posx // self.SQUARESIZE
        if self.is_valid_location(self.board, col):
            row = self.get_next_open_row(self.board, col)
            self.drop_piece(self.board, row, col, self.PLAYER_PIECE)

            if self.winning_move(self.board, self.PLAYER_PIECE):
                self.draw_board()
                messagebox.showinfo("Connect Four", "You WON!")
                self.root.destroy()
                return

            self.turn += 1
            self.turn = self.turn % 2

            self.print_board(self.board)
            self.draw_board()
            self.root.event_generate("<<UpdateGame>>", when="tail")

    def ai_move(self):
        col, minimax_score = self.minimax(self.board, 5, -math.inf, math.inf, True)
        if self.is_valid_location(self.board, col):
            row = self.get_next_open_row(self.board, col)
            self.drop_piece(self.board, row, col, self.AI_PIECE)

            if self.winning_move(self.board, self.AI_PIECE):
                messagebox.showinfo("Connect Four", "AI won!")
                self.root.destroy()
                return

            self.print_board(self.board)
            self.draw_board()
            self.turn += 1
            self.turn = self.turn % 2
            self.root.event_generate("<<UpdateGame>>", when="tail")

        if not self.game_over:
            self.root.after(500, self.play_game)

    def calculate_square_size(self):
        max_width = self.canvas.winfo_reqwidth()
        max_height = self.canvas.winfo_reqheight()

        square_size_width = max_width // self.COLUMN_COUNT
        square_size_height = max_height // (self.ROW_COUNT + 1)

        max_square_size_extrasmall = 90
        max_square_size_small = 78
        max_square_size_medium = 62
        max_square_size_smallmedium = 62
        max_square_size_large = 50

        if self.ROW_COUNT * self.COLUMN_COUNT <= 29:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_extrasmall)
        elif self.ROW_COUNT * self.COLUMN_COUNT <= 43:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_small)
        elif self.ROW_COUNT * self.COLUMN_COUNT <= 57:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_medium)
        elif self.ROW_COUNT * self.COLUMN_COUNT <= 65 and self.ROW_COUNT * self.COLUMN_COUNT != 63:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_smallmedium)
        else:
            SQUARESIZE = min(square_size_width, square_size_height, max_square_size_large)

        RADIUS = int(SQUARESIZE / 2)

        return SQUARESIZE, RADIUS

if __name__ == "__main__":
    game = ConnectFour(6, 7)