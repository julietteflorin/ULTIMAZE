

class new_Board():
    """This creats the Ultimate tic tac toe board"""
    def create_board(self):
        """Creates the board that contains only a tic tac toe. This is used for the main tic tac toe"""
        return [[0 for x in range(3)] for y in range(3)]

    def every_small_boards(self):
        """Creates the board contaning all the little tic tac toes"""
        return [[0 for y in range(9)] for z in range(9)]

    def reset(self, board, main_board, game_over):
        """This resets the board so that it is empty again and a new game can be played"""
        if game_over:
            for x,row in enumerate(board):
                for y in range(len(row)):
                    board[y][x] = 0

            for x,row in enumerate(main_board):
                for y in range(len(row)):
                    main_board[y][x] = 0
