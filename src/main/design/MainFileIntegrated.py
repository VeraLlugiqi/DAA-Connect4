import tkinter as tk
import numpy as np
import time
import sys
from backend_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, minimax, AI_PIECE, PLAYER_PIECE
from backend_logic import is_terminal_node

ROW_COUNT = 5
COLUMN_COUNT = 6
SQUARE_SIZE = 80
RADIUS = int(SQUARE_SIZE / 2)

class ConnectFourGUI2:
    def close_window(self):
        self.master.destroy()

    def __init__(self, master, player_name, row_count, column_count):
        self.player_name = player_name if player_name else "Player 1"  # Ensure a default name if not provided
        self.row_count = row_count
        self.column_count = column_count

        self.master = master
        self.master.title("Connect Four")

        connect_four_frame = tk.Frame(master, bg='red')
        connect_four_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        self.connect_four_label.pack(pady=10)

        button_frame = tk.Frame(master, bg='white')
        button_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='ew')

        self.name_label = tk.Label(button_frame, text=f'Name: {self.player_name}', font=('Helvetica', 14), bg='yellow', fg='black')
        self.name_label.pack(side='left', padx=20)

        tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

        self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=5, bg='yellow', fg='black')
        self.refresh_button.pack(side='left', padx=20)

        self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=5, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20)

        self.canvas = tk.Canvas(master, width=COLUMN_COUNT * SQUARE_SIZE, height=(ROW_COUNT + 1) * SQUARE_SIZE, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=2)

        self.board = create_board()
        self.draw_board()
        self.bind_events()

    def draw_board(self):
        self.canvas.delete("all")

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                # Drawing the rectangles (cells) with blue color
                self.canvas.create_rectangle(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                             (r + 2) * SQUARE_SIZE, fill='blue')
                # Drawing the circles (pieces) with white color
                self.canvas.create_oval(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                        (r + 2) * SQUARE_SIZE, fill='white')

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == PLAYER_PIECE:
                    # Player's piece (red circle)
                    self.canvas.create_oval(c * SQUARE_SIZE, (ROW_COUNT - r) * SQUARE_SIZE,
                                            (c + 1) * SQUARE_SIZE, (ROW_COUNT - r + 1) * SQUARE_SIZE,
                                            fill='red')
                elif self.board[r][c] == AI_PIECE:
                    # AI's piece (yellow circle)
                    self.canvas.create_oval(c * SQUARE_SIZE, (ROW_COUNT - r) * SQUARE_SIZE,
                                            (c + 1) * SQUARE_SIZE, (ROW_COUNT - r + 1) * SQUARE_SIZE,
                                            fill='yellow')

        x = (COLUMN_COUNT // 2) * SQUARE_SIZE
        y = SQUARE_SIZE * 0.5
        self.ball_id = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill='red')
        self.canvas.update()

    def bind_events(self):
        self.canvas.bind('<Motion>', self.on_mouse_motion)
        self.canvas.bind('<Button-1>', self.on_mouse_click)

    def on_mouse_motion(self, event):
        x = event.x
        y = SQUARE_SIZE * 0.5
        self.canvas.coords(self.ball_id, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)

    def on_mouse_click(self, event):
        x = event.x
        col = x // SQUARE_SIZE

        if is_valid_location(self.board, col):
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, PLAYER_PIECE)

            if winning_move(self.board, PLAYER_PIECE):
                self.display_winner("Player")
                return

            if is_terminal_node(self.board):
                self.display_winner("Tie")
                return

            self.draw_board()

        # AI's turn
        if not is_terminal_node(self.board):
            col, _ = minimax(self.board, 5, float('-inf'), float('inf'), True)
            print(f"AI moves to column {col}")
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, AI_PIECE)

            self.draw_board()

            if winning_move(self.board, AI_PIECE):
                print("AI wins!!")
                self.display_winner("AI")
                return

        if is_terminal_node(self.board):
            self.display_winner("Tie")

    def display_winner(self, winner):
        self.connect_four_label.config(text=f'Connect Four - {winner} wins!!', fg='red')

    def refresh(self):
        # Reset the game state
        self.board = create_board()
        self.draw_board()
        self.connect_four_label.config(text='Connect Four', fg='yellow')

    def get_player_name(self):
        return self.player_name

    def update_name_label(self, is_ai_turn=False):
        if is_ai_turn:
            truncated_name = "AI"
        else:
            truncated_name = self.get_truncated_player_name()
            self.name_label.config(text=truncated_name)


    def get_truncated_player_name(self):
        current_player_name = self.get_player_name()
        return current_player_name[:6].ljust(6)

if __name__ == "__main__":
    player_name = sys.argv[1] if len(sys.argv) > 1 else "Player 1"
    row_count = 6
    column_count = 7

    root = tk.Tk()
    app = ConnectFourGUI2(root, player_name, row_count, column_count)
    app.update_name_label()  # Update the name label initially
    root.mainloop()
