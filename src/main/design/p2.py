
import os
import tkinter as tk
import subprocess
import sys

def start_game():
    player1_name = sys.argv[1] if len(sys.argv) > 1 else "Player 1"
    player2_name = entry_emri.get()

    if player2_name:
        os.chdir("C:\\Users\\HP\\Desktop\\daaa\\connect4\\logic")

        command = ["python", "player_vs_player.py", player1_name, player2_name]
        
        # Check if playing against computer
        if "--computer" in sys.argv:
            command.append("--computer")

        subprocess.Popen(command)
        dritare_emri.destroy()
    else:
        etiketa_rezultati.config(text="Please enter a valid player name.")


# Krijo një dritare
dritare_emri = tk.Tk()
dritare_emri.title("")

# Krijo një etiketë për pyetjen
etiketa_pyetje = tk.Label(dritare_emri, text="Enter name for player 2:")
etiketa_pyetje.pack(pady=10)

# Krijo një kuti teksti për të shkruar emrin
entry_emri = tk.Entry(dritare_emri, font=("Arial", 12))
entry_emri.pack(pady=10)

# Krijo butonin "Start" për të shfaqur emrin
butoni_start = tk.Button(dritare_emri, text="Start", font=("Arial", 12), bg="red", width=15)
butoni_start.pack(pady=10)

# Krijo një etiketë për të shfaqur rezultatin
etiketa_rezultati = tk.Label(dritare_emri, text="", font=("Arial", 12))
etiketa_rezultati.pack(pady=10)

# Merr dimensionet e ekranit
gjeresia_ekrani = dritare_emri.winfo_screenwidth()
lartesia_ekrani = dritare_emri.winfo_screenheight()

# Merr dimensionet e dritares
gjeresia_dritare = 406
lartesia_dritare = 264

# Llogarit pozicionin për të vendosur dritaren në qendër të ekranit
pozicion_x = gjeresia_ekrani // 2 - gjeresia_dritare // 2
pozicion_y = lartesia_ekrani // 2 - lartesia_dritare // 2

# Vendos dimensionet dhe pozicionin e dritares
dritare_emri.geometry(f"{gjeresia_dritare}x{lartesia_dritare}+{pozicion_x}+{pozicion_y}")

# Run the Tkinter GUI
dritare_emri.mainloop()

