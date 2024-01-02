import tkinter as tk
from tkinter import messagebox
from datetime import datetime

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

		self.timer_label = tk.Label(button_frame, text='00:00', font=('Helvetica', 14), bg='lightgray')
		self.timer_label.pack(side='left', padx=20)

		tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

		button_width = 5
		self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
		self.refresh_button.pack(side='left', padx=20)

		self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
		self.close_button.pack(side='right', padx=20)

		self.update_timer()

	def update_timer(self):
		self.master.after(1000, self.update_timer) 

	def refresh(self):
		pass

	def close_window(self):
			self.master.destroy()

if __name__ == "__main__":
	root = tk.Tk()
	app = ConnectFourGUI(root)
	root.mainloop()
