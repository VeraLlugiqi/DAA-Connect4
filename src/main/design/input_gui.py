import subprocess
import tkinter as tk
import customtkinter
from tkinter import simpledialog
from tkinter import ttk

class ConnectFourSetup:
    def __init__(self):
        self.player_name = None
        self.grid_size = None

        self.window = tk.Tk()
        self.window.title("Connect Four Setup")
        self.window.geometry("900x700")
        self.window.configure(bg="white")

        header_frame = tk.Frame(self.window, bg="red")
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="PLAY CONNECT 4",  font=("Helvetica", 45, "bold"), bg="red", fg="yellow" ).pack(pady=50)

        padding_label = tk.Label(self.window, text="", bg="white")
        padding_label.pack(pady=15)

        tk.Label(self.window, text="Write your name:", bg="white",font=("Helvetica", 15)).pack(pady=10)
        self.name_entry = customtkinter.CTkEntry(self.window, placeholder_text="Your Name")
        self.name_entry.pack(pady=5) 

        tk.Label(self.window, text="Choose Table Size (rows x columns)",bg="white",font=("Helvetica", 15)).pack(pady=10)
        self.grid_size_var = customtkinter.StringVar()
        size_options = ["6x7", "5x4", "6x5", "8x7", "9x7", "10x7", "8x8"]
        size_dropdown = customtkinter.CTkComboBox(self.window, variable=self.grid_size_var, values=size_options)
        size_dropdown.set("6x7")  # Default value
        size_dropdown.pack(pady=5)

        tk.Label(self.window, text="Game Mode:",bg="white",font=("Helvetica", 15)).pack(pady=5)
        self.grid_size_var = customtkinter.StringVar()
        size_options = ["User vs User", "User vs Comp"]
        size_dropdown = customtkinter.CTkComboBox(self.window, variable=self.grid_size_var, values=size_options)
        size_dropdown.set("User vs Comp")  # Default value
        size_dropdown.pack(pady=5)

        
        button = customtkinter.CTkButton(master=self.window, corner_radius=10,text="Start", fg_color=("red", "lightgray"), command=self.submit_callback)
        button.pack(pady=20)


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
