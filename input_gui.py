import subprocess
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk

class ConnectFourSetup:
    def __init__(self):
        self.player_name = None
        self.grid_size = None

        self.window = tk.Tk()
        self.window.title("Connect Four Setup")
        self.window.geometry("500x300")

        tk.Label(self.window, text="What is your name?").pack(pady=10)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=10)

        tk.Label(self.window, text="Choose Table Size (rows x columns):").pack(pady=10)
        self.grid_size_var = tk.StringVar()
        size_options = ["5x4", "6x5", "8x7", "9x7", "10x7", "8x8"]
        size_dropdown = ttk.Combobox(self.window, textvariable=self.grid_size_var, values=size_options)
        size_dropdown.set("Select Size")
        size_dropdown.pack(pady=10)

        tk.Button(self.window, text="Submit", command=self.submit_callback).pack(pady=20)

    def get_player_name(self):
        return self.name_entry.get()

    def get_grid_size(self):
        return self.grid_size_var.get()

    def submit_callback(self):
        self.player_name = self.get_player_name()
        self.grid_size = self.get_grid_size()

        if not self.player_name or not self.grid_size:
           print("Please enter your name and choose the table size first.")
           return

        row_count, column_count = map(int, self.grid_size.split("x"))

        print(f"Player Name: {self.player_name}")
        print(f"Grid Size: {self.grid_size}")

    # Close the setup window
        self.window.destroy()

        print("Launching Connect Four game...")
        subprocess.Popen(["python", "connect4.py", self.player_name, str(row_count), str(column_count)])


if __name__ == "__main__":
    setup = ConnectFourSetup()
    setup.window.mainloop()
