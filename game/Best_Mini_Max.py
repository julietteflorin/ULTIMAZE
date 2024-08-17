import math
from Main_code.Board import new_Board
from Main_code.Frontend import Draw_pieces, draw_board, draw_big_pieces, Winner
from Main_code.Check_game import (
    Check_horizontally,
    Check_vertically,
    Check_diagonals,
    Check_Big_Board,
    empty_cells_big_board,
    empty_cells_small_boards,
    get_possible_moves,
    valid_locations,
    set_locations,
    check_game,
)

# Constants for player identification
Player_red = 1
Player_pink = -1
EMPTY = 0


matrice = [[2,1,2],[1,3,1],[2,1,2]]

def adjacence (plateau, x, y):
    """It gives a bonus when there are other flowers of ours but 0 for the opponent in the same row/column."""
    modif = 0
    j = plateau[x][y]
    for i in [1, 2]:
        if plateau[x][(y+i)%3] == j and plateau[x][(y-i)%3] != -j:
             modif += j
    for i in [1, 2]:
        if plateau[(x+i)%3][y] == j and plateau[(x-i)%3][y] != -j:
             modif += j
    return modif

def verif_win (plateau):
    """Verify the the board"""

    if plateau[0][0]==plateau[1][1] and plateau[0][0]==plateau[2][2]:
            return plateau[0][0]
    elif plateau[2][0]==plateau[1][1] and plateau[2][0]==plateau[0][2]:
            return plateau[2][0]
    elif plateau[2][0]==plateau[2][1] and plateau[2][0]==plateau[2][2]:
            return plateau[2][0]
    elif plateau[1][0]==plateau[1][1] and plateau[1][0]==plateau[1][2]:
            return plateau[1][0]
    elif plateau[0][0]==plateau[0][1] and plateau[0][0]==plateau[0][2]:
            return plateau[0][0]
    elif plateau[0][1]==plateau[1][1] and plateau[0][1]==plateau[2][1]:
            return plateau[0][1]
    elif plateau[0][2]==plateau[1][2] and plateau[0][2]==plateau[2][2]:
            return plateau[0][2]
    elif plateau[0][0]==plateau[1][0] and plateau[0][0]==plateau[2][0]:
            return plateau[0][0]
    else : return 0
    

def eval(plateau, decali, decalj) :
    """Evaluation of a mal board"""
    board = [[0,0,0],[0,0,0],[0,0,0]]

    for i in range (3):
        for j in range (3):
            
            board[i][j]=plateau[i +decali][j + decalj]
    
    
    score = 0
    for i in range (3):
        for j in range (3):
            if plateau[i + decali][j + decalj] != 2:
                score += plateau[i + decali][j + decalj] * matrice[i][j]
                score += adjacence(board, i, j)
    return score


def evaluate(Main_board, Board):
    """Evaluation function that returns the score of a certain board disposition"""
    k = verif_win(Main_board)
    if k != 0 :
        return k * 100000

    score = 0
    for i in range (3) :
        for j in range (3):
            if Main_board[i][j] == 0 :
                k = eval(Board, 3*i, 3*j)
                score += k* matrice[i][j]
            else :
                score += matrice[i][j] * Main_board[i][j] * 20


    return score

def minmax(main_board, small_boards, depth, alpha, beta, maximizing_player, box):
    """MinMax algorithm with alpha-beta pruning."""
    if depth == 0 or Check_Big_Board(main_board,Player_red) != 0 or Check_Big_Board(main_board, Player_pink) !=0 or box == []:
        return evaluate(main_board, small_boards)


    if maximizing_player:
        # If it is the Maximizing player that playes
        max_eval = -math.inf
        # Lets try every move and chose the best one
        for move in box:
            y, x = move
            # Play the move
            small_boards[y][x] = Player_red
            check_game(small_boards, main_board, Player_red)
            check_game(small_boards, main_board, Player_pink)
            box = get_possible_moves(small_boards, x, y,main_board)
            # Lets try with this move
            eval = minmax(main_board, small_boards, depth - 1, alpha, beta, False, box)
            # Lets go back to the original game
            small_boards[y][x] = 0
            main_board = [[0,0,0],
                          [0,0,0],
                          [0,0,0]]
            check_game(small_boards, main_board, Player_red)
            check_game(small_boards, main_board, Player_pink)
            # Chose the best branche
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        # The minimizer player playes
        min_eval = math.inf
        for move in box:
            # Chose a move
            y, x = move
            # Play the move
            small_boards[y][x]  = Player_pink
            check_game(small_boards, main_board, Player_red)
            check_game(small_boards, main_board, Player_pink)
            box = get_possible_moves(small_boards, x, y,main_board)
            # Continue trying the branche
            eval = minmax(main_board, small_boards, depth - 1, alpha, beta, True, box)
            # Go back to inicial parameters
            small_boards[y][x] = 0
            main_board = [[0,0,0],
                          [0,0,0],
                          [0,0,0]]
            check_game(small_boards, main_board, Player_red)
            check_game(small_boards, main_board, Player_pink)
            # Evaluate the best move for the minimizer
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(main_board, small_boards, player, box, depth):
    """Finds the best move for the current player."""
    best_val = -math.inf if player == Player_red else math.inf
    best_move = None
    for move in box:
        y, x = move
        small_boards[y][x] = player
        box = get_possible_moves(small_boards, x, y,main_board)
        move_val = minmax(main_board, small_boards, depth, -math.inf, math.inf, player == Player_red, box)
        small_boards[y][x] = 0
        if (player == Player_red and move_val > best_val) or (player == Player_pink and move_val < best_val):
            best_val = move_val
            best_move = move
    return best_move

