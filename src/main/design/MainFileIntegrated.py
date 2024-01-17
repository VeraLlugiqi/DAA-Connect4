# MainFileIntegrated.py
import tkinter as tk
import threading
import time
import sys
from backend_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, minimax, AI_PIECE, PLAYER_PIECE
from backend_logic import is_terminal_node
from p1 import create_confirmation_window

ROW_COUNT = 5
COLUMN_COUNT = 6

class ConnectFourGUI2:
    def close_window(self):
        create_confirmation_window(self.close)

    def close(self):
        self.master.destroy()  

    def __init__(self, master, player_name, row_count, column_count):
        self.player_name = player_name if player_name else "Player 1"  # Ensure a default name if not provided
        self.row_count = row_count
        self.column_count = column_count
        self.start_time = None

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
        connect_four_frame.grid(row=0, column=0, columnspan=10, sticky='ew')

        for i in range(10):
            master.columnconfigure(i, weight=1)

        self.connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        self.connect_four_label.pack(pady=10)

        button_frame = tk.Frame(master, bg='white')
        button_frame.grid(row=1, column=0, columnspan=10, pady=20, sticky='ew')

        self.name_label = tk.Label(button_frame, text=f'Name: {self.player_name}', font=('Helvetica', 14), bg='yellow', fg='black')
        self.name_label.pack(side='left', padx=20)

        self.time_var = tk.StringVar(value='04:00')
        self.timer_label = tk.Label(button_frame, textvariable=self.time_var, font=('Helvetica', 14), bg='lightgray',width=10)
        self.timer_label.pack(side='left', padx=(250, 70), anchor='center')

        tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

        self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=5, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20, anchor='e')  

        self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=5, bg='yellow', fg='black')
        self.refresh_button.pack(side='right', padx=(20, 20))

        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=10)

        self.square_size = 0
        self.radius = 0
        self.calculate_square_size()

        self.board = create_board(row_count, column_count)  # Pass row_count and column_count to create_board
        self.draw_board()
        self.bind_events()

        self.game_in_progress = True
        self.stop_timer_event = threading.Event()
        self.start_timer_thread()
        self.end_time = None

    
    def  start_timer_thread(self):
        self.start_time = time.time()
        timer_thread = threading.Thread(target=self.count_down)
        timer_thread.start()

    def count_down(self):
        total_in_seconds = 4 * 60

        while total_in_seconds >= 0:
            if self.stop_timer_event.is_set():
                break

            minutes, seconds = divmod(total_in_seconds, 60)
            time_str = f'{minutes:02d}:{seconds:02d}'
            self.time_var.set(time_str)
            self.master.update()
            time.sleep(1)
            total_in_seconds -= 1
            
            if not self.game_in_progress:
               break
        if not self.stop_timer_event.is_set():
           self.end_time = time.strftime("%H:%M:%S")
           self.time_var.set("00:00")
           self.master.after(1000, self.complete_count_down)
    def complete_count_down(self):
    # Check if the player won or lost
      if not self.stop_timer_event.is_set():
        self.open_result_window()
        self.game_in_progress = False
        self.end_time = None 
    def open_result_window(self):
        # Set the stop event to signal the timer thread to stop
        self.stop_timer_event.set()            
    def update_timer_label(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            time_str = f'{minutes:02d}:{seconds:02d}'
            self.timer_label.config(text=time_str)

            # Schedule the next update after 1000 milliseconds (1 second)
            self.master.after(1000, self.update_timer_label)   

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
        self.canvas.delete("all")

        for c in range(self.column_count):
            for r in range(self.row_count):
                # Drawing the rectangles (cells) with blue color
                self.canvas.create_rectangle(c * self.square_size, (r + 1) * self.square_size, (c + 1) * self.square_size,
                                             (r + 2) * self.square_size, fill='blue', outline='blue')
                # Drawing the circles (pieces) with white color
                self.canvas.create_oval(c * self.square_size, r * self.square_size + self.square_size, (c + 1) * self.square_size,
                                        (r + 1) * self.square_size + self.square_size, fill='white')

        for c in range(self.column_count):
            for r in range(self.row_count-1, -1, -1):
                if self.board[r][c] == PLAYER_PIECE:
                    # Player's piece (red circle)
                    self.canvas.create_oval(c * self.square_size, (r + 1) * self.square_size,
                                            (c + 1) * self.square_size, (r + 2) * self.square_size,
                                            fill='red')
                elif self.board[r][c] == AI_PIECE:
                    # AI's piece (yellow circle)
                    self.canvas.create_oval(c * self.square_size, (r + 1) * self.square_size,
                                            (c + 1) * self.square_size, (r + 2) * self.square_size,
                                            fill='yellow')

        x = (self.column_count // 2) * self.square_size
        y = self.square_size * 0.5 - self.square_size  # Adjusted to be one row above the table
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

            self.draw_board()

            if winning_move(self.board, PLAYER_PIECE):
                self.display_winner("Player")
                self.game_in_progress = False
                return

            if is_terminal_node(self.board):
                self.display_winner("Tie")
                self.game_in_progress = False
                return
            

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
                self.game_in_progress = False
                return
            self.draw_board()
            i=0
            for r in range(self.row_count):
                if self.board[r][self.column_count-1] != 0:
                    i+=1
            if i == self.row_count:
                self.open_draw_window()
                   


    def display_winner(self, winner):
        if winner == "Player":
            self.open_win_window()
        elif winner == "AI":
            self.open_loss_window()
        else:
            self.connect_four_label.config(text=f'Connect Four - {winner} Tied!', fg='red')

    def open_win_window(self):
        self.stop_timer_event.set()
        import winner_box
        winner_box.winnerBox("You won!", self.refresh, self.master)

    def open_loss_window(self):
        self.stop_timer_event.set()
        import loser_box
        loser_box.loserBox("You lost!", self.refresh, self.master, self.master)

    def open_draw_window(self):
        self.stop_timer_event.set()
        import loser_box
        loser_box.loserBox("IT'S A TIE!", self.refresh, self.master, self.master)


    def refresh(self):
        # Reset the game state
        self.game_in_progress = True
        self.board = create_board(self.row_count, self.column_count)
        self.draw_board()
        self.connect_four_label.config(text='Connect Four', fg='yellow')
        self.start_timer_thread()


        
        

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
