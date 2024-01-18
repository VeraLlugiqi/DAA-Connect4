import tkinter as tk

def create_confirmation_window(callback):
    dritare = tk.Tk()
    dritare.title("")

    etiketa_pyetje = tk.Label(dritare, text="Are you sure?", font=("Arial", 12))
    etiketa_pyetje.pack(pady=20)

    madhesia_butonave = 10

    def on_yes():
        callback()
        dritare.destroy()

    butoni_po = tk.Button(dritare, text="Yes", font=("Arial", 12), bg="red", width=madhesia_butonave, relief=tk.GROOVE, command=on_yes)
    butoni_po.pack(side=tk.LEFT, padx=50)

    def on_no():
        dritare.destroy()

    butoni_jo = tk.Button(dritare, text="No", font=("Arial", 12), bg="red", width=madhesia_butonave, relief=tk.GROOVE, command=on_no)
    butoni_jo.pack(side=tk.RIGHT, padx=50)

    gjeresia_ekrani = dritare.winfo_screenwidth()
    lartesia_ekrani = dritare.winfo_screenheight()

    gjeresia_dritare = 406
    lartesia_dritare = 264

    pozicion_x = gjeresia_ekrani // 2 - gjeresia_dritare // 2
    pozicion_y = lartesia_ekrani // 2 - lartesia_dritare // 2

    dritare.geometry(f"{gjeresia_dritare}x{lartesia_dritare}+{pozicion_x}+{pozicion_y}")

    dritare.mainloop()

if __name__ == "__main__":
	create_confirmation_window("")
   