import tkinter as tk
import numpy as np
import sys

from player_vs_ai_zana01 import ConnectFour

class ConnectFourGUI(tk.Frame):
    def __init__(self, master, player1_name, player2_name, row_count, column_count):
        super().__init__(master)
        self.row_count = row_count
        self.column_count = column_count
        self.master.title("Connect Four")
        self.master.configure(bg="white")
        self.master.resizable(width=False, height=False)
        self.player1_name = player1_name
        self.player2_name = player2_name

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

        self.refresh_button = tk.Button(self.button_frame, text='🔄', command=self.do_refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.refresh_button.pack(side='right', padx=(20, 20))
        self.canvas = tk.Canvas(master, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=10)
        self.canvas_id = self.canvas.create_text(10, 10, anchor="nw")


    def do_refresh(self):
        self.board = np.zeros((self.row_count, self.column_count))
        self.game_over = False
        self.current_player = 1
        self.update_name_label()
        self.canvas.delete('all')
        self.calculate_square_size()
        self.draw_board()    

    def refresh(self):
        if self.timer_thread and self.timer_thread.is_alive():
          self.timer_thread.join()

        self.total_seconds_p1 = 4 * 60
        self.total_seconds_p2 = 4 * 60
        self.elapsed_time_p1 = 0
        self.elapsed_time_p2 = 0

        self.board = np.zeros((self.row_count, self.column_count))
        self.game_over = False
        self.current_player = 1
        self.update_name_label()
        self.canvas.delete('all')
        self.calculate_square_size()
        self.draw_board()

        # Start a new timer thread
        self.start_timer_thread()

    def close_window(self):
        create_confirmation_window(self.close)

    def close(self):
        self.master.destroy()

    def draw_game(self, board):
        self.canvas.delete(self.canvas_id)  

        game_text = '\n'.join([' '.join(map(str, row)) for row in board])
        self.canvas.itemconfig(self.canvas_id, text=game_text)


if __name__ == "__main__":           
    root = tk.Tk()
    gui = ConnectFourGUI(root, "", "", 1, 2)
    #game = ConnectFour(gui, 1, 2)  
    root.mainloop()
