import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
from datetime import datetime

#for table 
import numpy as np
import pygame
import sys

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

		self.time_var = tk.StringVar(value='04 : 00')
		self.time_lbl = tk.Label(font=('Arial', 14), textvariable=self.time_var, bg='lightgray')
		self.time_lbl.grid(row=1, column=0, padx=20)

		tk.Label(button_frame, text='', bg='white').pack(side='left', padx=50)

		button_width = 5
		self.refresh_button = tk.Button(button_frame, text='🔄', command=self.refresh, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
		self.refresh_button.pack(side='left', padx=20)

		self.close_button = tk.Button(button_frame, text='❌', command=self.close_window, font=('Helvetica', 12), width=button_width, bg='yellow', fg='black')
		self.close_button.pack(side='right', padx=20)

		self.count_down()

	def count_down(self):
		total_in_seconds = 4 * 60

		while total_in_seconds >= 0:
			minutes, seconds = divmod(total_in_seconds, 60)
			time_str = f'{minutes:02d} : {seconds:02d}'
			self.time_var.set(time_str)
			self.master.update()
			time.sleep(1)
			total_in_seconds -= 1

		self.time_var.set("00 : 00")
		self.open_result_window()

	def open_result_window(self):
		result_window = tk.Toplevel(self.master)
		result_window.title("Result Window")

		label = tk.Label(result_window, text="Timer reached 00:00", font=('Arial', 16))
		label.pack(padx=20, pady=20)


	def refresh(self):
		pass

	def close_window(self):
			self.master.destroy()

if __name__ == "__main__":
	root = tk.Tk()
	app = ConnectFourGUI(root)
	root.mainloop()


#table part
BLUE = 	(176,224,230)
PINK = (250,240,230)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece


def print_board(board):
	print(np.flip(board, 0))

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, PINK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 80

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/3)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 60)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, PINK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, PINK, (0,0, width, SQUARESIZE))
			print(event.pos)