import tkinter as tk
import numpy as np
import time
from backend_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, minimax, AI_PIECE, PLAYER_PIECE
from backend_logic import is_terminal_node

ROW_COUNT = 5
COLUMN_COUNT = 6
SQUARE_SIZE = 80
RADIUS = int(SQUARE_SIZE / 2)

class ConnectFourGUI:
    def close_window(self):
        self.master.destroy()

    def __init__(self, master):

        self.master = master
        self.master.title("Connect Four")

        connect_four_frame = tk.Frame(master, bg='red')
        connect_four_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        self.connect_four_label.pack(pady=10)

        button_frame = tk.Frame(master, bg='white')
        button_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='ew')

        self.name_label = tk.Label(button_frame, text='\u200bName:', font=('Helvetica', 14), bg='yellow', fg='black')
        self.name_label.pack(side='left', padx=20)

        tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

        self.time_var = tk.StringVar(value='04 : 00')
        self.time_lbl = tk.Label(font=('Arial', 14), textvariable=self.time_var, bg='lightgray')
        self.time_lbl.grid(row=1, column=0, padx=20)

        tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

        button_width = 5
       # self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        #self.refresh_button.pack(side='left', padx=20)

        self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20)

        self.canvas = tk.Canvas(master, width=COLUMN_COUNT * SQUARE_SIZE, height=(ROW_COUNT + 1) * SQUARE_SIZE, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=2)

        self.board = create_board()
        self.draw_board()
        self.bind_events()
      #  self.count_down(240)

    def draw_board(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                self.canvas.create_rectangle(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                             (r + 2) * SQUARE_SIZE, fill='blue')
                self.canvas.create_oval(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                        (r + 2) * SQUARE_SIZE, fill='white')

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == PLAYER_PIECE:
                    self.canvas.create_oval(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                            (r + 2) * SQUARE_SIZE, fill='red')
                elif self.board[r][c] == AI_PIECE:
                    self.canvas.create_oval(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                            (r + 2) * SQUARE_SIZE, fill='yellow')

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
            self.draw_board()

    def display_winner(self, winner):
        self.connect_four_label.config(text=f'Connect Four - {winner} wins!!', fg='red')

      
  # Add any additional logic you want when the game is over

def refresh(self):
    pass

    def count_down(self, total_seconds):
        while total_seconds >= 0:
            minutes, seconds = divmod(total_seconds, 60)
            time_str = f'{minutes:02d} : {seconds:02d}'
            self.time_var.set(time_str)
            self.master.update()
            time.sleep(1)
            total_seconds -= 1

        self.time_var.set("00 : 00")
        self.open_result_window()

    def open_result_window(self):
        result_window = tk.Toplevel(self.master)
        result_window.title("Result Window")

        label = tk.Label(result_window, text="Timer reached 00:00", font=('Arial', 16))
        label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()
