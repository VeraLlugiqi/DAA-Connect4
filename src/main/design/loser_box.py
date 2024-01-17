import tkinter as tk
import subprocess

def close_window(window):
    window.destroy()

def on_closing(window, master):
    master.destroy()  # Call your additional function
    window.destroy()


def option_selected(option, refresh_function, window_to_destroy, main_game_window):
    print(option)
    if option == "Play Again":
        refresh_function()
        window_to_destroy.destroy()
    elif option == "Home":
        window_to_destroy.destroy()
        main_game_window.destroy()
        open_input_gui(main_game_window)


def open_input_gui(main_game_window):
    subprocess.run(["python", "input_gui.py"])
    # main_game_window.destroy()

def create_rounded_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command)
    button.config(width=15, height=2, bd=0, bg='red', fg='black', font=('Helvetica', 12))
    return button

def loserBox(message, refresh_function, main_game_window, master):
    window = tk.Tk()
    window.title("AlertBox")
    window.geometry("406x264+{0}+{1}".format((window.winfo_screenwidth() - 406) // 2, (window.winfo_screenheight() - 264) // 2))
    window.attributes('-toolwindow', True)
    window.attributes('-topmost', 1)

    frame = tk.Frame(window)

    def play_again():
        option_selected("Play Again", refresh_function, window, main_game_window)

    button1 = create_rounded_button(frame, "Home", lambda: option_selected("Home", refresh_function, window, main_game_window))
    button2 = create_rounded_button(frame, "Play Again", play_again)

    frame.pack(side="bottom", pady=10)
    button1.pack(side="left", padx=10)
    button2.pack(side="right", padx=10)

    tk.Label(window, text=message, font=("Helvetica", 20)).place(relx=0.5, rely=0.30, anchor="n")
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, master))

    window.mainloop()

if __name__ == "__main__":
    def refresh_function():
        print("Refresh function called")

    main_game_window = tk.Tk()
    main_game_window.title("Main Game Window")
    main_game_window.geometry("800x600")
    main_game_window.mainloop()

    winnerBox("You won", refresh_function, main_game_window)
