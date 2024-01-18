# backend_logic.py
import numpy as np

PLAYER_PIECE = 1
AI_PIECE = 2

def create_board(rows, cols):
    return np.zeros((rows, cols), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(len(board[0]) - 3):
        for r in range(len(board)):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for a win
    for c in range(len(board[0])):
        for r in range(len(board) - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(len(board[0]) - 3):
        for r in range(len(board) - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(len(board[0]) - 3):
        for r in range(3, len(board)):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(len(board[0])):
        row = get_next_open_row(board, col)
        if row is not None:
            valid_locations.append(col)
    return valid_locations

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, evaluate_board(board))

    if maximizing_player:
        value = float('-inf')
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing player
        value = float('inf')
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def evaluate_board(board):
    score = 0

    # Center column score
    center_array = [int(i) for i in list(board[:, len(board[0]) // 2])]
    center_count = center_array.count(PLAYER_PIECE)
    score += center_count * 3

    # Horizontal score
    for r in range(len(board)):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(len(row_array) - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, PLAYER_PIECE)

    # Vertical score
    for c in range(len(board[0])):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(len(col_array) - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, PLAYER_PIECE)

    # Positive diagonal score
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, PLAYER_PIECE)

    # Negative diagonal score
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, PLAYER_PIECE)

    return score

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score
