import subprocess
import tkinter as tk
import customtkinter
import os
import sys
sys.path.append("..")
from logic.player_vs_player import ConnectFourGUI
from logic.player_vs_ai_zana01 import ConnectFour
from MainFileIntegrated import ConnectFourGUI2

class ConnectFourSetup:
    def __init__(self):
        self.player_name = None
        self.grid_size = None
        self.game_mode = None

        self.window = tk.Tk()
        self.window.title("Connect Four Setup")
        adjusted_width = 900  # Adjust this value based on your preference
        adjusted_height = 700  # Adjust this value based on your preference
        self.window.geometry(f"{adjusted_width}x{adjusted_height}")
        extra_right_margin = 200  # Adjust this value based on your preference
        extra_top_margin = 50
        self.window.geometry("+%d+%d" % ((self.window.winfo_screenwidth() - adjusted_width + extra_right_margin) // 2,
                               (self.window.winfo_screenheight() - adjusted_height - extra_top_margin) // 2))

        self.window.configure(bg="white")

        header_frame = tk.Frame(self.window, bg="red")
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="PLAY CONNECT 4",  font=("Helvetica", 45, "bold"), bg="red", fg="yellow" ).pack(pady=50)

        padding_label = tk.Label(self.window, text="", bg="white")
        padding_label.pack(pady=15)

        input_frame = tk.Frame(self.window, bg="white")
        input_frame.pack(pady=10)

        tk.Label(self.window, text="Choose Table Size (rows x columns)",bg="white",font=("Helvetica", 15)).pack(pady=10)
        self.grid_size_var = customtkinter.StringVar()
        size_options = ["6x7", "5x4", "6x5", "8x7", "9x7", "10x7", "8x8"]
        size_dropdown = customtkinter.CTkComboBox(self.window, variable=self.grid_size_var, values=size_options)
        size_dropdown.set("6x7")  # Default value
        size_dropdown.pack(pady=5)

        tk.Label(self.window, text="Game Mode:", bg="white", font=("Helvetica", 15)).pack(pady=5)

        button_frame = tk.Frame(self.window, bg="white")
        button_frame.pack(pady=5)

        user_vs_user_button = tk.Button(button_frame, text="🧑 vs 🧑", font=("Helvetica", 22), command=self.start_user_vs_user_popup, width=15, height=3, bg="yellow")
        user_vs_user_button.pack(side="left", padx=10)

        user_vs_comp_button = tk.Button(button_frame, text="🧑 vs 💻", font=("Helvetica", 22), command=self.start_user_vs_comp_popup, width=15, height=3, bg="yellow")        
        user_vs_comp_button.pack(side="left", padx=10)
        user_vs_comp_button.pack(side="left", padx=10)
    def set_game_mode(self, mode):
        self.game_mode = mode

    def get_grid_size(self):
        return self.grid_size_var.get()

    def submit_callback(self):
        self.player_name = self.get_player_name()
        self.grid_size = self.get_grid_size()

    def start_user_vs_user_popup(self):
        # Create a new window for player names
        popup_window = tk.Toplevel(self.window)
        popup_window.title("Enter Player Names")
        popup_window.configure(bg="white")

        header_frame = tk.Frame(popup_window, bg="red")
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="Enter Player Names", font=("Helvetica", 18, "bold"), bg="red", fg="yellow").pack(pady=10)

        tk.Label(popup_window, text="Enter Player 1 name:", font=("Helvetica", 12), bg="white").pack(pady=5)
        entry_player1 = tk.Entry(popup_window, font=("Helvetica", 12), validate="key", validatecommand=(popup_window.register(self.validate_entry), "%P"))
        entry_player1.pack(pady=5)

        tk.Label(popup_window, text="Enter Player 2 name:", font=("Helvetica", 12), bg="white").pack(pady=5)
        entry_player2 = tk.Entry(popup_window, font=("Helvetica", 12), validate="key", validatecommand=(popup_window.register(self.validate_entry), "%P"))
        entry_player2.pack(pady=5)

        button_frame = tk.Frame(popup_window, bg="white")
        button_frame.pack(pady=10)

        start_button = tk.Button(button_frame, text="Start Game", command=lambda: self.start_user_vs_user_game(entry_player1.get(), entry_player2.get(), popup_window), font=("Helvetica", 14), width=15, height=2, bg="yellow", fg="black")
        start_button.pack()

        # Center the popup window
        popup_window.geometry("300x270")
        popup_window.geometry("+%d+%d" % ((self.window.winfo_screenwidth() - popup_window.winfo_reqwidth()) // 2,
                                          (self.window.winfo_screenheight() - popup_window.winfo_reqheight()) // 2))

        entry_player1.focus_set()

    def validate_entry(self, text):
        return len(text) <= 5

    def start_user_vs_user_game(self, player1, player2, popup_window):
        player_name1 = player1
        player_name2 = player2
        grid_size = self.grid_size_var.get()

        row_count, column_count = map(int, grid_size.split("x"))

        print(f"Grid Size: {grid_size}")

        # Close the popup window
        popup_window.destroy()
        self.window.destroy()

        # Create an instance of ConnectFourGUI
        root = tk.Tk()
        game_instance = ConnectFourGUI(root, player_name1, player_name2, row_count, column_count)
        root.mainloop()

    def start_user_vs_comp_popup(self):
        # Create a new window for player name
        popup_window = tk.Toplevel(self.window)
        popup_window.title("Enter Player Name")
        popup_window.configure(bg="white")

        header_frame = tk.Frame(popup_window, bg="red")
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="Enter Your Name", font=("Helvetica", 18, "bold"), bg="red", fg="yellow").pack(pady=10)

        tk.Label(popup_window, text="Enter Your Name:", font=("Helvetica", 12), bg="white").pack(pady=5)
        entry_player = tk.Entry(popup_window, font=("Helvetica", 12), validate="key", validatecommand=(popup_window.register(self.validate_entry), "%P"))
        entry_player.pack(pady=5)

        button_frame = tk.Frame(popup_window, bg="white")
        button_frame.pack(pady=10)

        start_button = tk.Button(button_frame, text="Start Game", command=lambda: self.start_user_vs_comp_game(entry_player.get(), popup_window), font=("Helvetica", 14), width=15, height=2, bg="yellow", fg="black")
        start_button.pack()

            # Center the popup window
        popup_window.geometry("300x270")
        popup_window.geometry("+%d+%d" % ((self.window.winfo_screenwidth() - popup_window.winfo_reqwidth()) // 2,
                                              (self.window.winfo_screenheight() - popup_window.winfo_reqheight()) // 2))

        entry_player.focus_set()

    def start_user_vs_comp_game(self, player, popup_window):
        player_name = player
        grid_size = self.grid_size_var.get()

        row_count, column_count = map(int, grid_size.split("x"))

        print(f"Grid Size: {grid_size}")

        # Close the popup window
        popup_window.destroy()
        self.window.destroy()

        #root = tk.Tk()
        #game_instance = ConnectFourGUI2(root, player_name, row_count, column_count)
        #root.mainloop()

        game_instance = ConnectFour(row_count, column_count)
        game_instance.play_game()


if __name__ == "__main__":
    setup = ConnectFourSetup()
    setup.window.mainloop()
