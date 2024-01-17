# DAA-Connect4
# Project Overview
Connect Four Game 

Course: Design and Analysis of Algorithms

Overview: Implement a program to play Connect Four. The program should take as input the Connect Four board and output the moves to win the game.

Description: This project was coded in Python using the library Tkinter and implementing the Alpha Beta Pruning and Minmax Algorithms. 
The game is a traditional Connect Four game played by choosing the table size from various sizes offered in a dropbox and choosing between player vs player or player vs AI. 


# Requirements
	Functional Requirements:
		Accept any valid Connect Four board as input.
		Output optimal moves to win the game using the Minimax Algorithm.
	Non-functional Requirements:
		Response time for move calculation should be reasonable.
# Algorithm:
 Minimax Algorithm explores the game tree by recursively simulating possible moves up to a specified depth (depth parameter). For each explored move, it assigns a score based on the resulting game state. The scores are then propagated back up the tree, and the algorithm chooses the move with the highest score if it's the maximizing player's turn or the move with the lowest score if it's the minimizing player's turn.
To improve efficiency, alpha-beta pruning is applied. This technique reduces the number of nodes evaluated by the minimax algorithm by eliminating branches that are guaranteed not to affect the final decision.
 If at any point during exploration, the algorithm determines that a branch's score won't affect the final decision (i.e., alpha is greater than or equal to beta), it prunes that branch, saving computational resources.
# Milestones:


![Screenshot (701)](https://github.com/VeraLlugiqi/DAA-Connect4/assets/115923848/ccfd594d-cfbe-4f4d-baf5-bcb3116e90f5)

Photo 1. The division of tasks in different epics

![Screenshot (700)](https://github.com/VeraLlugiqi/DAA-Connect4/assets/115923848/121f2354-3401-4100-85d7-91f1b7404d12)

Photo 2. Branch protection (master and developer)


![Screenshot (702)](https://github.com/VeraLlugiqi/DAA-Connect4/assets/115923848/bd2aea25-be3e-404b-9db6-320f78576592)
Photo 3. The activity of the students.


![Screenshot (689)](https://github.com/VeraLlugiqi/DAA-Connect4/assets/115923848/172edaf6-6e81-4f9d-9060-2bdade5756a5)

Photo 4. The backlog of a sprint.


![Screenshot (705)](https://github.com/VeraLlugiqi/DAA-Connect4/assets/115923848/175dab01-b9db-4bc3-9f30-0330dfde476f)
Photo 5. A sprint view in different statuses.


![0-02-05-48016d2bfdfade0bdd2683cc992cd351bd642cf9ee0d1c842151588815d9fdc7_9a426e715fd5faa1](https://github.com/VeraLlugiqi/DAA-Connect4/assets/115923848/f7cd1163-93ef-4135-87d6-59f2ec9ec38a)

Photo 6. An example of a winning and losing game.


# User Manuals:
To play the game from local host one can clone it directly from this gihub, 
	Execute the input_gui.py file, 
	Pick the table size and mode(player vs player or player vs AI)
	The game will continue until one of the players wins or runs out of time, 
	The game can end in a tie or using the buttons the game can be refreshed or exited.
If playing on web:
	Upon opening the main page pick the preferences and enjoy the game.

# Project Closure
	Outcomes:
	Despite the moves of the player, AI is able to identify and play the moves to win the game.
# Project Team
	Anjeza Sfishta
	Leonite Gllareva
	Medina Shabani
	Rinesa Zuzaku
	Tringa Baftiu
	Valtrina Cacaj
	Vera Llugiqi
	Zana Misini
