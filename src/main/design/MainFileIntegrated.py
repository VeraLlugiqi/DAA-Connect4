# MainFileIntegrated.py
import time
import tkinter as tk
import sys
from backend_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, minimax, AI_PIECE, PLAYER_PIECE
from backend_logic import is_terminal_node
import numpy as np

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
        self.timer_running = False
        self.total_seconds = 240
        self.winner = None
        

        self.master = master
        self.master.title("Connect Four")
        adjusted_width = 900  # Adjust this value based on your preference
        adjusted_height = 700  # Adjust this value based on your preference
        self.master.geometry(f"{adjusted_width}x{adjusted_height}")
        self.master.configure(bg="white")

    # Center the window on the screen
        extra_right_margin = 200  # Adjust this value based on your preference
        extra_top_margin = 50
        self.master.geometry("+%d+%d" % ((self.master.winfo_screenwidth() - adjusted_width + extra_right_margin) // 2,
                               (self.master.winfo_screenheight() - adjusted_height - extra_top_margin) // 2))

        connect_four_frame = tk.Frame(master, bg='red')
        connect_four_frame.grid(row=0, column=0, columnspan=10, sticky='nsew')
        for i in range(10):
            master.columnconfigure(i, weight=1)

        self.connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        self.connect_four_label.pack(pady=10)

        button_frame = tk.Frame(master, bg='white')
        button_frame.grid(row=1, column=0, columnspan=10, pady=20, sticky='ew')

        self.name_label = tk.Label(button_frame, text=f'Name: {self.player_name}', font=('Helvetica', 14), bg='yellow', fg='black')
        self.name_label.pack(side='left', padx=20)

        tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

        self.timer_label = tk.Label(button_frame, text='00:00', font=('Helvetica', 14), bg='lightgray')
        self.timer_label.pack(side='left', padx=(160, 30), anchor='center')

        self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=5, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20, anchor='e')

        self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=5, bg='yellow', fg='black')
        self.refresh_button.pack(side='right', padx=(20, 20))

        # self.canvas = tk.Canvas(master, width=column_count * SQUARE_SIZE, height=(row_count + 1) * SQUARE_SIZE, bg='white')
        # self.canvas.grid(row=2, column=0, columnspan=2)

        # self.board = create_board(row_count, column_count)  # Pass row_count and column_count to create_board
        # self.draw_board()
        # self.bind_events()

        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.grid(row=2,column=0,columnspan=10)


        self.row_count = row_count
        self.column_count = column_count
        self.square_size = 0
        self.radius = 0


        self.calculate_square_size()
        self.board = np.zeros((self.row_count, self.column_count))
        self.ball_id = None

        self.draw_board()
        self.bind_events()
        self.update_name_label()

    
    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
      if self.total_seconds > 0 and self.timer_running:
        minutes, seconds = divmod(self.total_seconds, 60)
        time_str = f'{minutes:02d}:{seconds:02d}'
        self.timer_label.config(text=time_str)
        self.total_seconds -= 1
        self.master.after(1000, self.update_timer)  # schedule the next update after 1000 milliseconds (1 second)
      else:
        self.timer_label.config(text='00:00')
        if self.timer_running:  # Check if the timer was running
            if self.winner == "AI":
                    winner_text = "AI wins!"
            else:
                winner_text = f'{self.player_name} wins!'
            self.timer_label.config(text=winner_text, bg='yellow')
            self.show_result() 
            self.timer_running = False

    def stop_timer(self):
        self.timer_running = False

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

        if self.row_count * self.column_count <= 29:  # percaktojme madhesine e tabeles madhe/vogel
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
        # self.canvas.delete("all")

        for c in range(self.column_count):
            for r in range(self.row_count + 1):
                fill_color = 'white' if r == 0 else 'blue'
                outline_color = 'white' if r == 0 else 'blue'  
                self.canvas.create_rectangle(c * self.square_size, r * self.square_size, (c + 1) * self.square_size,
                                             (r + 1) * self.square_size, fill=fill_color, outline=outline_color)
                if r > 0:
                    self.canvas.create_oval(c * self.square_size, r * self.square_size, (c + 1) * self.square_size,
                                             (r + 1) * self.square_size, fill='white')
        for c in range(self.column_count):
             for r in reversed(range(self.row_count)):
                if self.board[r][c] == PLAYER_PIECE:
                    # Player's piece (red circle)
                    self.canvas.create_oval(c * self.square_size, (r+1) * self.square_size, (c + 1) * self.square_size,
                                             (r + 2) * self.square_size, fill='red')
                elif self.board[r][c] == AI_PIECE:
                    # AI's piece (yellow circle)
                    self.canvas.create_oval(c * self.square_size, (r+1) * self.square_size, (c + 1) * self.square_size,
                                             (r + 2) * self.square_size, fill='yellow')

        x = (self.column_count // 2) * self.square_size
        y = 0.5 * self.square_size
        self.ball_id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill='red')

        self.canvas.update()
       



    def bind_events(self):
        self.canvas.bind('<Motion>', self.on_mouse_motion)
        self.canvas.bind('<Button-1>', self.on_mouse_click)

    def on_mouse_motion(self, event):
        x = event.x
        y = self.square_size * 0.5
        self.canvas.coords(self.ball_id, x - self.radius, y - self.radius, x + self.radius, y + self.radius)

    def on_mouse_click(self, event):
        x = event.x
        col = x // self.square_size

        if is_valid_location(self.board, col):
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, PLAYER_PIECE)

            if winning_move(self.board, PLAYER_PIECE):
                self.winner = "Player"
                self.display_winner(self.player_name)
                return

            if is_terminal_node(self.board):
                self.winner = "Tie"
                self.display_winner("Tie")
                return

            self.draw_board()
            self.stop_timer()
            self.start_timer()
            

        # AI's turn
        if not is_terminal_node(self.board):
            col, _ = minimax(self.board, 5, float('-inf'), float('inf'), True)
            print(f"AI moves to column {col}")
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, AI_PIECE)
            self.draw_board()

            if winning_move(self.board, AI_PIECE):
                print("AI wins!!")
                self.winner = "AI"
                self.display_winner("AI")
                return
            self.draw_board()
            self.stop_timer()
            self.start_timer()    

    def display_winner(self, winner):
        if winner == "Player":
            self.stop_timer()
            self.open_win_window()
        elif winner == "AI":
            self.stop_timer()
            self.open_loss_window()
        else:
            self.stop_timer()
            self.connect_four_label.config(text=f'Connect Four - {winner} Tied!', fg='red')
            
        self.stop_timer()
    def open_win_window(self):
        import winner_box
        self.stop_timer()

    def open_loss_window(self):
        import loser_box
        self.stop_timer()

    def refresh(self):
        # Reset the game state
        self.board = create_board(self.row_count, self.column_count)
        self.draw_board()
        self.connect_four_label.config(text='Connect Four', fg='yellow')
        self.stop_timer()
        self.timer_label.config(text='00:00')

    def get_player_name(self):
        return self.player_name

    def update_name_label(self, is_ai_turn=False):
        if is_ai_turn:
            truncated_name = "AI"
        else:
            truncated_name = self.get_truncated_player_name()
            self.name_label.config(text=truncated_name)
            self.stop_timer()

    def get_truncated_player_name(self):
        current_player_name = self.get_player_name()
        return current_player_name[:6].ljust(6)

    def refresh(self):
        self.total_seconds = 240  # Reset the timer to the initial value
        self.board = create_board(self.row_count, self.column_count)
        self.draw_board()
        self.connect_four_label.config(text='Connect Four', fg='yellow')
        self.stop_timer()
        self.timer_label.config(text='00:00')
if __name__ == "__main__":
    player_name = sys.argv[1] if len(sys.argv) > 1 else "Player 1"
    row_count = 6
    column_count = 7

    root = tk.Tk()
    app = ConnectFourGUI2(root, player_name, row_count, column_count)
    app.update_name_label()  # Update the name label initially
    root.mainloop()
