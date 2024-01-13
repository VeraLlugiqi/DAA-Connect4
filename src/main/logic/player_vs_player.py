import tkinter as tk
import numpy as np
import sys

class ConnectFourGUI(tk.Frame):
    def __init__(self, master, player1_name, player2_name, row_count, column_count):
        super().__init__(master)
        self.master.title("Connect Four")
        self.master.configure(bg="white")
        self.master.resizable(width=False, height=False)
        self.player1_name = player1_name
        self.player2_name = player2_name




        adjusted_width = 900  # Adjust this value based on your preference
        adjusted_height = 700  # Adjust this value based on your preference
        self.master.geometry(f"{adjusted_width}x{adjusted_height}")
        self.master.configure(bg="white")

    # Center the window on the screen
        extra_right_margin = 200  # Adjust this value based on your preference
        extra_top_margin = 50
        self.master.geometry("+%d+%d" % ((self.master.winfo_screenwidth() - adjusted_width + extra_right_margin) // 2,
                               (self.master.winfo_screenheight() - adjusted_height - extra_top_margin) // 2))

        self.current_player = 1  
        self.game_over = False

        connect_four_frame = tk.Frame(master, bg='red')
        connect_four_frame.grid(row=0, column=0, columnspan=10 ,sticky='nsew')

        for i in range(10):
            master.columnconfigure(i, weight=1)

        connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        connect_four_label.pack(pady=10)

        self.button_frame = tk.Frame(master, bg='white')
        self.button_frame.grid(row=1, column=0, columnspan=10, pady=20, sticky='ew')

        self.name_frame = tk.Frame(self.button_frame, bg='white')
        self.name_frame.pack(side='left', padx=20)

        self.name_label = tk.Label(self.name_frame, text='', font=('Helvetica', 14), bg='yellow', fg='black', width=5)
        self.name_label.pack()

        tk.Label(self.button_frame, text='', bg='white').pack(side='left', padx=50)

        self.timer_label = tk.Label(self.button_frame, text='00:00', font=('Helvetica', 14), bg='lightgray')
        self.timer_label.pack(side='left', padx=(160, 30), anchor='center')

        tk.Label(self.button_frame, text='', bg='white', width=10).pack(side='left')


        button_width = 5
        self.close_button = tk.Button(self.button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20, anchor='e')  

        self.refresh_button = tk.Button(self.button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.refresh_button.pack(side='right', padx=(20, 20))

        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=10)

        self.row_count = row_count
        self.column_count = column_count
        self.square_size = 0  #marrim square size dinamikisht nga metoda calulcate_square_size
        self.radius = 0  

        self.calculate_square_size()
        self.board = np.zeros((self.row_count, self.column_count))
        self.ball_id = None  

        self.draw_board()
        self.bind_events()
        self.update_name_label()

    def calculate_square_size(self):
        max_width = self.master.winfo_screenwidth()
        max_height = self.master.winfo_screenheight()

        square_size_width = max_width // self.column_count
        square_size_height = max_height // (self.row_count + 1)  

        # i percaktojna dimensionet sa me u kon ni square nqs tabela ma e vogel / madhe
        max_square_size_extrasmall = 90
        max_square_size_small = 78
        max_square_size_medium = 62
        max_square_size_smallmedium = 62
        max_square_size_large = 50

        if self.row_count * self.column_count <= 31:  # percaktojme madhesine e tabeles madhe/vogel
            self.square_size = min(square_size_width, square_size_height, max_square_size_extrasmall)
        elif self.row_count * self.column_count <= 43:  # percaktojme madhesine e tabeles madhe/vogel
            self.square_size = min(square_size_width, square_size_height, max_square_size_small)
        elif self.row_count * self.column_count <= 57:  
            self.square_size = min(square_size_width, square_size_height, max_square_size_medium)
        elif self.row_count * self.column_count <= 65 and self.row_count * self.column_count!=63:  
            self.square_size = min(square_size_width, square_size_height, max_square_size_smallmedium)   
        else:
            self.square_size = min(square_size_width, square_size_height, max_square_size_large)

        self.radius = int(self.square_size / 2)

        canvas_width = self.column_count * self.square_size
        canvas_height = (self.row_count + 1) * self.square_size  
        self.canvas.config(width=canvas_width, height=canvas_height)

    def draw_board(self):
       
        for c in range(self.column_count):
            for r in range(self.row_count + 1):
                fill_color = 'white' if r == 0 else 'blue'
                outline_color = 'white' if r == 0 else 'blue'  
                self.canvas.create_rectangle(c * self.square_size, r * self.square_size, (c + 1) * self.square_size,
                                             (r + 1) * self.square_size, fill=fill_color, outline=outline_color)
                if r > 0:
                    self.canvas.create_oval(c * self.square_size, r * self.square_size, (c + 1) * self.square_size,
                                             (r + 1) * self.square_size, fill='white')

        x = (self.column_count // 2) * self.square_size
        y = 0.5 * self.square_size
        color = 'red' if self.current_player == 1 else 'yellow'
        self.ball_id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=color)

        self.canvas.update()

    def bind_events(self):
        self.canvas.bind('<Motion>', self.on_mouse_motion)
        self.canvas.bind('<Button-1>', self.on_mouse_click)

    def on_mouse_motion(self, event):
        if not self.game_over:
            x = event.x
            y = self.square_size * 0.5
            color = 'red' if self.current_player == 1 else 'yellow'
            self.canvas.coords(self.ball_id, x - self.radius, y - self.radius, x + self.radius, y + self.radius)
            self.canvas.itemconfig(self.ball_id, fill=color)

    def on_mouse_click(self, event):
        if not self.game_over:
            col = event.x // self.square_size
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
                self.update_name_label()
                self.timer_label.config(text='00:00', bg='lightgray')

    def get_next_open_row(self, col):
        for r in range(len(self.board) - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def draw_piece(self, row, col):
        x = (col + 0.5) * self.square_size
        y = (row + 1.5) * self.square_size 
        color = 'red' if self.current_player == 1 else 'yellow'
        self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill=color)
        self.canvas.update()

    def check_win(self, row, col):
        player = self.board[row][col]

        # Check horizontally
        if col <= self.column_count - 4:
            if np.all(self.board[row, col:col + 4] == player):
                return True

        # Check vertically
        if row <= self.row_count - 4:
            if np.all(self.board[row:row + 4, col] == player):
                return True

        # Check diagonally (positive slope)
        if row <= self.row_count - 4 and col <= self.column_count - 4:
            if np.all([self.board[row + i, col + i] == player for i in range(4)]):
                return True

        # Check diagonally (negative slope)
        if row >= 3 and col <= self.column_count - 4:
            if np.all([self.board[row - i, col + i] == player for i in range(4)]):
                return True

        return False

    def check_draw(self):
        return np.all(self.board != 0)

    def refresh(self):
        self.board = np.zeros((self.row_count, self.column_count))
        self.game_over = False
        self.current_player = 1
        self.update_name_label()
        self.timer_label.config(text='00:00', bg='lightgray')
        self.canvas.delete('all')
        self.calculate_square_size()
        self.draw_board()

    def close_window(self):
        self.master.destroy()

    #Merr emrin e player
    def get_player_name(self, player):
        if player == 1:
            return self.player1_name
        elif player == 2:
            return self.player2_name
        else:
            return ""

    def update_name_label(self):
        truncated_name = self.get_truncated_player_name()
        self.name_label.config(text=truncated_name)

    def get_truncated_player_name(self):
        current_player_name = self.get_player_name(self.current_player)
        return current_player_name[:6].ljust(6)


if __name__ == "__main__":
    player1_name = sys.argv[1] if len(sys.argv) > 1 else "Player 1"
    player2_name = sys.argv[2] if len(sys.argv) > 2 else "Player 2"
    row_count = 6
    column_count = 7

    root = tk.Tk()
    app = ConnectFourGUI(root, player1_name, player2_name, row_count, column_count)
    root.mainloop()
