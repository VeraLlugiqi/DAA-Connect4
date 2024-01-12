import tkinter as tk
import numpy as np
import sys

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 80
RADIUS = int(SQUARE_SIZE / 2)


class ConnectFourGUI(tk.Frame):
    def __init__(self, master, player1_name, player2_name, row_count, column_count):
        super().__init__(master)
        self.master.title("Connect Four")

        self.player1_name = player1_name
        self.player2_name = player2_name

        self.current_player = 1  # Player 1 starts
        self.game_over = False

        connect_four_frame = tk.Frame(master, bg='red')
        connect_four_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        connect_four_label.pack(pady=10)

		button_frame = tk.Frame(master, bg='white')
		button_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='ew')

		self.name_label = tk.Label(button_frame, text='\u200bName:', font=('Helvetica', 14), bg='yellow', fg='black')
		self.name_label.pack(side='left', padx=20)

		tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

		self.timer_label = tk.Label(self.button_frame, text='00:00', font=('Helvetica', 14), bg='lightgray')
        self.timer_label.pack(side='left', padx=20)

        tk.Label(self.button_frame, text='', bg='white').pack(side='left', padx=50)

        button_width = 5
        self.refresh_button = tk.Button(self.button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.refresh_button.pack(side='left', padx=20)

        self.close_button = tk.Button(self.button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20)

        self.canvas = tk.Canvas(master, width=column_count * SQUARE_SIZE, height=(row_count + 1) * SQUARE_SIZE, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=2)

        self.board = np.zeros((row_count, column_count))
        self.ball_id = None  # To store the ID of the drawn ball

        self.draw_board()
        self.bind_events()
    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                self.canvas.create_rectangle(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                             (r + 2) * SQUARE_SIZE, fill='blue')
                self.canvas.create_oval(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE,
                                         (r + 2) * SQUARE_SIZE, fill='pink')

        x = (COLUMN_COUNT // 2) * SQUARE_SIZE
        y = SQUARE_SIZE * 0.5
        color = 'red' if self.current_player == 1 else 'yellow'
        self.ball_id = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill=color)

        self.canvas.update()    
    def bind_events(self):
        self.canvas.bind('<Motion>', self.on_mouse_motion)
        self.canvas.bind('<Button-1>', self.on_mouse_click)

    def on_mouse_motion(self, event):
        if not self.game_over:
            x = event.x
            y = SQUARE_SIZE * 0.5
            color = 'red' if self.current_player == 1 else 'yellow'
            self.canvas.coords(self.ball_id, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)
            self.canvas.itemconfig(self.ball_id, fill=color)    
    def on_mouse_click(self, event):
        if not self.game_over:
            col = event.x // SQUARE_SIZE
            self.drop_piece(col)    
    def drop_piece(self, col):
        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = self.current_player
            self.draw_piece(row, col)

            if self.check_win(row, col):
                self.game_over = True
                winner = f'{self.get_player_name(self.current_player)} wins!'
                self.timer_label.config(text=winner, bg='yellow')

            elif self.check_draw():
                self.game_over = True
                self.timer_label.config(text='It\'s a draw!', bg='yellow')

            else:
                self.current_player = 3 - self.current_player  # Switch player
                self.name_label.config(text=f'{self.get_player_name(self.current_player)}')
                self.timer_label.config(text='00:00', bg='lightgray')            