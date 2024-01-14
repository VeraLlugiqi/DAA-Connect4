import tkinter as tk

def create_confirmation_window(callback):
    # Create a Tkinter window
    dritare = tk.Tk()
    dritare.title("")

    # Create a label with the question
    etiketa_pyetje = tk.Label(dritare, text="Are you sure?", font=("Arial", 12))
    etiketa_pyetje.pack(pady=20)

    # Set the size of the buttons
    madhesia_butonave = 10

    # Create two buttons for "Yes" and "No" with the same size
    def on_yes():
        callback()
        dritare.destroy()

    butoni_po = tk.Button(dritare, text="Yes", font=("Arial", 12), bg="red", width=madhesia_butonave, relief=tk.GROOVE, command=on_yes)
    butoni_po.pack(side=tk.LEFT, padx=50)

    def on_no():
        dritare.destroy()

    butoni_jo = tk.Button(dritare, text="No", font=("Arial", 12), bg="red", width=madhesia_butonave, relief=tk.GROOVE, command=on_no)
    butoni_jo.pack(side=tk.RIGHT, padx=50)

    # Get the screen dimensions
    gjeresia_ekrani = dritare.winfo_screenwidth()
    lartesia_ekrani = dritare.winfo_screenheight()

    # Get the window dimensions
    gjeresia_dritare = 406
    lartesia_dritare = 264

    # Calculate the position to center the window on the screen
    pozicion_x = gjeresia_ekrani // 2 - gjeresia_dritare // 2
    pozicion_y = lartesia_ekrani // 2 - lartesia_dritare // 2

    # Set the dimensions and position of the window
    dritare.geometry(f"{gjeresia_dritare}x{lartesia_dritare}+{pozicion_x}+{pozicion_y}")

    # Run the Tkinter GUI
    dritare.mainloop()

# Call the function to create the confirmation window
if __name__ == "__main__":
	create_confirmation_window("")
   