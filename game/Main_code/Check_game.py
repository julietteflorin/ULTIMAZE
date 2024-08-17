from  Main_code.Frontend  import Draw_pieces, draw_board, draw_big_pieces, Winner

def valid_locations(board,main_board,x,y, box):
    """This checks that where the player chose to play is a an empty spot where it is possible to play"""
    if box == None or [x,y] in box:
        if board[y][x] == 0 and main_board[y//3][x//3] == 0:
            return True
    return False


def set_locations(board,main_board, x,y, player, box):
    """This plays puts the players move into the board"""
    if valid_locations(board,main_board,x,y, box):
        board[y][x] = player
        return True
    else:
        return False


def get_next_box(x,y, small_boards, main_board):
    """This returns the positions possible in the box of where the next player must play"""
    for i in range(0,8,3):
        for j in range(0,8,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(3):
                    for h in range(3):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards, main_board)
                else :
                    return possible_moves
    

    for i in range(0,7,3):
        for j in range(1,8,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(3):
                    for h in range(3,6):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards, main_board)
                else :
                    return possible_moves
    

    for i in range(0,8,3):
        for j in range(2,9,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(3):
                    for h in range(6,9):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards, main_board)
                else :
                    return possible_moves
    

    for i in range(1,8,3):
        for j in range(0,7,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(3,6):
                    for h in range(3):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards, main_board)
                else :
                    return possible_moves
    

    for i in range(1,8,3):
        for j in range(1,8,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(3,6):
                    for h in range(3,6):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards,main_board)
                else :
                    return possible_moves
    

    for i in range(1,8,3):
        for j in range(2,9,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(3,6):
                    for h in range(6,9):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards, main_board)
                else :
                    return possible_moves
    

    for i in range(2,9,3):
        for j in range(0,9,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(6,9):
                    for h in range(3):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards,main_board)
                else :
                    return possible_moves
    

    for i in range(2,9,3):
        for j in range(1,9,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(6,9):
                    for h in range(3,6):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards,main_board)
                else :
                    return possible_moves
    

    for i in range(2,9,3):
        for j in range(2,9,3):
            if (x,y) == (i,j):
                possible_moves = []
                for k in range(6,9):
                    for h in range(6,9):
                        if small_boards[h][k] == 0 :
                            possible_moves.append([k,h])
                if possible_moves == []:
                    return empty_cells_small_boards(small_boards, main_board)
                else :
                    return possible_moves
    

def get_possible_moves(Board, x,y, main_board):
    """Gives all the possible positions that are possible in the small box if it is not won"""
    # Get the box if the box is won
    if main_board[y%3][x%3] != 0:
        Box = empty_cells_small_boards(Board, main_board)

    # Get the box if the box is not won 
    else :
        Box = get_next_box(x,y,Board, main_board)

        # Let's take out all the elements that are taken
    return Box

def place_big_board(main_board,x, y, player):
    """This places the winner of the big tic tac toe"""
    main_board[y][x] = player

def empty_cells_small_boards(board, main_board):
    """Let's return all the empty cells on the small boards"""
    empty_cells = []
    for y,row in enumerate(board): 
        for x,case in enumerate(row):
            if case == 0 and main_board[y//3][x//3] == 0:
                empty_cells.append([x,y])
    return empty_cells

def empty_cells_big_board(main_board):
    """Let's return all the empty cells on the big board"""
    empty_cells = []
    for x,row in enumerate(main_board):
        for y,case in enumerate(row):
            if case == 0:
                empty_cells.append([x,y])
    return empty_cells

def place_small_board(small_boards, x, y, player):
    """This places a value if the box has been won"""
    for pos in range(0,3):
        y_new = y*3 + pos
        for pos2 in range(0,3):
            x_new = x*3 + pos2
            small_boards[y_new][x_new] = player
def Check_horizontally(board, main_board, player):
    """Checks for horizontal wins and places the win"""

    for x in range(0,9,3):
        for y, row in enumerate(board):
            if row[x] == row[1+x] == row[2+x] == player:
                place_big_board(main_board,x//3,y//3,player)

def Check_vertically(board,main_board, player, AI = False):
    """Checks for vertically wins and places the win"""
    # We check every 3 rows 
    for x in range(0,9):
        for y in range(0,9,3):
            if board[y][x] == board[y+1][x] == board[y+2][x] == player :
                place_big_board(main_board,x//3,y//3,player)


def Check_diagonals(board, main_board, player):
    """Checks for diagonal wins and places the win"""
    for x in range(0,9,3):
        #print(x)
        stock_indx = []
        for y in range(0,9,3):
            #print(x,y)
            stock_indx.append(board[y][x])
            for i in range(1,3):
                stock_indx.append(board[y+i][x+i])
                
                if len(stock_indx) >= 3:
                    if stock_indx.count(player) == len(stock_indx):
                        a,b = y+i, x+i
                        #print(player, "succeeds with a negative diagonal")
                        place_big_board(main_board, b//3, a//3, player)
                        stock_indx.clear()

                    else:
                        stock_indx.clear()

    for x in range(0,8,3):
        stock_nindx = []
        for y in range(2,9,3):
            #print(x,y)
            for i in range(3):
                stock_nindx.append(board[y-i][x+i])

                if len(stock_nindx) >= 3:
                    #print(stock_nindx)
                    if stock_nindx.count(player) == len(stock_nindx):
                        a,b = y-i, x+i
                        #print(player, "succeeds with a negative diagonal")
                        place_big_board(main_board, b//3, a//3, player)
                        stock_nindx.clear()
                    else:
                        stock_nindx.clear()




def Check_Big_Board(main_board, player):
    """Checks the big board for wins"""
    for row in main_board:
        row_stock = []
        for i in range(len(main_board)):
            row_stock.append(row[i])
        if row_stock.count(player) == len(row_stock):
            return player

    for col in range(len(main_board)):
        col_stock = []
        for row in main_board:
            col_stock.append(row[col])
        if col_stock.count(player) == len(col_stock) and col_stock[0] != 0:
            return player

    diag_1 = []
    for indx in range(len(main_board)):
        diag_1.append(main_board[indx][indx])
    if len(diag_1) == diag_1.count(player):
        return player


    diag_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(main_board)))):
        diag_2.append(main_board[indx][rev_indx])
    
    if diag_2.count(player) == len(diag_2):
        return player


    if len(empty_cells_big_board(main_board)) == 0:
        return 2
    
    return 0


def check_game(board,main_board, player):
    """Checks wins on all the small tic tac toes"""
    #Check horizontally
    Check_horizontally(board, main_board, player)

    #Check vertically
    Check_vertically(board, main_board, player)

    #Check diagonals
    Check_diagonals(board, main_board, player)

