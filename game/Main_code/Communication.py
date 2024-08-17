import hashlib

def calculate_position_to_send(x, y):
    """This transferes our postitions into the convention of the protocol"""
    bs = (y // 3)*3 + (x // 3)
    ss = (y % 3)*3 + (x % 3)
    return bs, ss

def calculate_position_received(bs, ss):
    """This transfered the positions given by the client into a position we can put in our code"""
    x = (bs % 3) * 3 + ss % 3
    y = (bs//3) * 3 + ss // 3 
    return x, y

def haching_function(state_game):
    """Hached the state of the game"""
    m = hashlib.sha3_224()
    m.update(state_game)    #b"010101101-.........-........./0.......1-....1....-........./.........-....1....-1...0...."
    return m.hexdigest()

def text_state_game(small_board):
    """
    Convert our game to the text to hach 
    ex: b"010101101-.........-........./0.......1-....1....-........./.........-....1....-1...0....              
    """
    d={0:".",1:"1",-1:"0"}
    text = ""
    for j in range(9):
        oy = (j//3)*3
        ox = (j%3)*3
        if j!=0:
            if j%3==0:
                text+="/"
            else:
                text+="-"
        for i in range(9):
            text+=d[small_board[oy +i//3][ox+i%3]]

    return text.encode()
    
