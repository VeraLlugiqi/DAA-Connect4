import tkinter as tk
import numpy as np
import time
from datetime import datetime

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 80
RADIUS = int(SQUARE_SIZE / 2)

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")

        connect_four_frame = tk.Frame(master, bg='red')
        connect_four_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        connect_four_label = tk.Label(connect_four_frame, text='Connect Four', font=('Helvetica', 24), bg='red', fg='yellow')
        connect_four_label.pack(pady=10)

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
        self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.refresh_button.pack(side='left', padx=20)

        self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
        self.close_button.pack(side='right', padx=20)

        self.canvas = tk.Canvas(master, width=COLUMN_COUNT * SQUARE_SIZE, height=(ROW_COUNT + 2) * SQUARE_SIZE, bg='white')
        self.canvas.grid(row=2, column=0, columnspan=2)

        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.ball_id = None  # To store the ID of the drawn ball


        self.draw_board()
        self.bind_events()
        self.count_down()

    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                self.canvas.create_rectangle(c * SQUARE_SIZE, (r + 1)* SQUARE_SIZE, (c + 1) * SQUARE_SIZE, (r + 2) * SQUARE_SIZE, fill='blue')
                self.canvas.create_oval(c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, (c + 1) * SQUARE_SIZE, (r + 2) * SQUARE_SIZE, fill='pink')

        # Adjusted starting position for the ball
        x = (COLUMN_COUNT // 2) * SQUARE_SIZE
        y = SQUARE_SIZE * 0.5 
        self.ball_id = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill='red')

        self.canvas.update()

    def bind_events(self):
        self.canvas.bind('<Motion>', self.on_mouse_motion)

    def on_mouse_motion(self, event):
        x = event.x
        y = SQUARE_SIZE * 0.5 
        self.canvas.coords(self.ball_id, x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS)

    def refresh(self):
        pass

    def close_window(self):
        self.master.destroy()

    def count_down(self):
        total_in_seconds = 4 * 60

        while total_in_seconds >= 0:
            minutes, seconds = divmod(total_in_seconds, 60)
            time_str = f'{minutes:02d} : {seconds:02d}'
            self.time_var.set(time_str)
            self.master.update()
            time.sleep(1)
            total_in_seconds -= 1

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
