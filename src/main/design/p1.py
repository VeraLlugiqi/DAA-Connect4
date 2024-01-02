import tkinter as tk
from tkinter import messagebox

# Krijo një dritare
dritare = tk.Tk()
dritare.title("")

# Krijo një etiketë me pyetjen
etiketa_pyetje = tk.Label(dritare, text="Are you sure?", font=("Arial", 12))
etiketa_pyetje.pack(pady=20)

# Përcakto madhësinë e butonave
madhesia_butonave = 10

# Krijo dy butona për "Po" dhe "Jo" me madhësi të njëjtë
butoni_po = tk.Button(dritare, text="Yes", font=("Arial", 12), bg="red", width=madhesia_butonave, relief=tk.GROOVE)
butoni_po.pack(side=tk.LEFT, padx=50)

butoni_jo = tk.Button(dritare, text="No", font=("Arial", 12), bg="red", width=madhesia_butonave, relief=tk.GROOVE)
butoni_jo.pack(side=tk.RIGHT, padx=50)

# Merr dimensionet e ekranit
gjeresia_ekrani = dritare.winfo_screenwidth()
lartesia_ekrani = dritare.winfo_screenheight()

# Merr dimensionet e dritares
gjeresia_dritare = 400
lartesia_dritare = 264

# Llogarit pozicionin për të vendosur dritaren në qendër të ekranit
pozicion_x = gjeresia_ekrani // 2 - gjeresia_dritare // 2
pozicion_y = lartesia_ekrani // 2 - lartesia_dritare // 2

# Vendos dimensionet dhe pozicionin e dritares
dritare.geometry(f"{gjeresia_dritare}x{lartesia_dritare}+{pozicion_x}+{pozicion_y}")

# Run the Tkinter GUI
dritare.mainloop()

