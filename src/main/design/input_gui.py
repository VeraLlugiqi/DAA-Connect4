import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class ConnectFourSetup:
    def __init__(self):
        self.player_name = None
        self.grid_size = None

        self.window = tk.Tk()
        self.window.title("Connect Four Setup")
        self.window.geometry("500x400")

        header_frame = tk.Frame(self.window, bg="red")
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="PLAY CONNECT 4", font=("Helvetica", 16), bg="red").pack(pady=10)


        tk.Label(self.window, text="Write your name:").pack(pady=5)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        tk.Label(self.window, text="Pick the board size:").pack(pady=5)
        self.grid_size_var = tk.StringVar()
        size_options = ["5x4", "6x5", "8x7", "9x7", "10x7", "8x8"]
        size_dropdown = ttk.Combobox(self.window, textvariable=self.grid_size_var, values=size_options)
        size_dropdown.set("6x7")  # Default value
        size_dropdown.pack(pady=5)

        tk.Label(self.window, text="Game Mode:").pack(pady=5)
        mode_var = tk.StringVar()
        mode_var.set("User vs User")
        mode_dropdown = ttk.Combobox(self.window, textvariable=mode_var, values=["User vs User", "User vs Comp"])
        mode_dropdown.pack(pady=5)

        # Placeholder images, replace them with your actual images
        photo1 = tk.PhotoImage(width=50, height=50)
        photo2 = tk.PhotoImage(width=50, height=50)

        # Display placeholder images
        tk.Label(self.window, image=photo1).pack(side=tk.LEFT, padx=10)
        tk.Label(self.window, image=photo2).pack(side=tk.RIGHT, padx=10)

        # tk.Label(self.window, text="vs").pack(pady=5)

        tk.Button(self.window, text="Start", command=self.submit_callback,bg="red").pack(pady=20)

    def get_player_name(self):
        return self.name_entry.get()

    def get_grid_size(self):
        return self.grid_size_var.get()

    # def get_game_mode(self):
    #     return mode_var.get()

    def submit_callback(self):
        self.player_name = self.get_player_name()
        self.grid_size = self.get_grid_size()
        game_mode = self.get_game_mode()

        if not self.player_name or not self.grid_size:
            print("Please enter your name and choose the table size first.")
            return

        row_count, column_count = map(int, self.grid_size.split("x"))

        print(f"Player Name: {self.player_name}")
        print(f"Grid Size: {self.grid_size}")
        print(f"Game Mode: {game_mode}")

        # Close the setup window
        self.window.destroy()

        print("Launching Connect Four game...")
        subprocess.Popen(["python", "connect4.py", self.player_name, str(row_count), str(column_count), game_mode])


if __name__ == "__main__":
    setup = ConnectFourSetup()
    setup.window.mainloop()
