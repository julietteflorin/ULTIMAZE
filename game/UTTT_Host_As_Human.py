
import cv2
import socket
import mediapipe as mp
import pyautogui
import matplotlib.pyplot as plt
import math
import threading
import time
import pygame
import os
# Import modules containing game logic and functionality
from Main_code.hand_det import Quit_game, go_left, go_right, go_down, go_up, place
from Main_code.Board import new_Board
from Main_code.Communication import calculate_position_received, calculate_position_to_send, haching_function, text_state_game
from Main_code.Frontend import Draw_pieces, draw_board, draw_big_pieces, Winner, update_window
from Main_code.Check_game import (
    Check_horizontally,
    Check_vertically,
    Check_diagonals,
    Check_Big_Board,
    empty_cells_big_board,
    get_possible_moves,
    valid_locations,
    set_locations,
    check_game,
)
# Initialize font for text rendering
pygame.font.init()

# Define the Host 
host = ""
port = 12000
     
def main():
    """
    The main game loop that handles events, updates the game state, and renders the display.
    """

    # Create connection with the other RasberryPI and wait for someone to connect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        while True:
            s, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(s, addr))
            client_thread.start()
            
def handle_client(s, addr):
    """Playes as a Host and handles the client. The Host is a Humain that playes with the camera"""
            
    # Define screen dimensions
    Width, Height = 810, 810
    Screen_width = 1000
    Square = Width // 3  # Divide into 3 equal parts
    Small_Square = Square // 3  # Further divide each part into 3


    # Load image assets for game pieces
    Red_rose_small = pygame.transform.scale(
        pygame.image.load(os.path.join("Images", "rose.png")), (Small_Square, Small_Square)
    )
    Red_rose = pygame.transform.scale(
        pygame.image.load(os.path.join("Images", "rose.png")), (Square, Square)
    )
    Pink_rose_small = pygame.transform.scale(
        pygame.image.load(os.path.join("Images", "rose_rose.png")), (Small_Square, Small_Square)
    )
    Pink_rose = pygame.transform.scale(
        pygame.image.load(os.path.join("Images", "rose_rose.png")), (Square, Square)
    )

    # Define background and line colors
    Bg = (240, 223, 222)
    Lines_color = (11,81,0)
    Lines_color_2 = (14,108,0)
    Lines_color_red = (155,3,3) # Color for highlighting pieces 
    Lines_color_pink = (255,166,190) # Color for highlighting pieces 
    # Create an instance of the game board class
    Game_Board = new_Board()

    # Parameter of the camera 
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    frame_width, frame_height = (640,480)
    hand_y = 0
    clock = pygame.time.Clock()
    
    # Create the game window and set caption
    Window = pygame.display.set_mode((Screen_width, Height))
    pygame.display.set_caption("Ultimate Tic Tac Toe against other")
    clock = pygame.time.Clock()  # Used to control frame rate

    # Game settings
    FPS = 60  # Frames per second
    game_not_over = True
    pos_v=(360,360,90,90)
    # Game board variables
    box = None  # Tracks the currently selected small board within the bigger board
    main_board = Game_Board.create_board()  # Create the main board
    small_boards = Game_Board.every_small_boards()  # Create all small boards within the main board
    # Font for text
    font = pygame.font.Font('Precious.ttf', 40)

    # Text dimensions
    text_width = (Screen_width - Width)*2//3
    text_height = 50
    # Text of who plays positions
    text_x = Width + text_width//3
    text_y = Height//2 - (text_height*2 + Small_Square)//2
    # Position of button to play again
    Play_butt_y = text_y + text_height + Small_Square
    # Text of who plays text and next game
    Play_butt_text = font.render(u"Menu", True, (0,0,0))
    text1_text = font.render(u"Player:", True, (0,0,0))
    my_hash = haching_function(text_state_game(small_boards))
    # Time out for connection
    time_out = 10
    
    # Set who plays fist: the guest always starts
    turn = 1
    
    # Start the connection using the protocol
    time_sec = time.time()
    waiting_time = 0
    waiting = True
    while waiting == True :
        print("we have started to wait")
        data = s.recv(1024).decode()
        
        waiting_time = abs(time_sec - time.time())
        if data.startswith("UTTT/1.0 CONNECTION"):
            print("we got the message")
            s.sendall(f"UTTT/1.0 CONNECTION Ultimaze\n".encode())
            waiting = False
        elif waiting_time>=time_out or data.startswith("UTTT/1.0 406 FATAL_ERROR"):
            if waiting_time >= time_out:
                s.sendall(f"UTTT/1.0 406 FATAL_ERROR\n".encode())
            game_not_over = False
            waiting = False
            s.close()
            with open('Start.py')as new:
                exec(new.read())
        
    while game_not_over:
        # Limit frame rate for smooth gameplay
        clock.tick(FPS)
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame=cv2.resize(frame,(frame_width, frame_height))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        # The line cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) is in the code because OpenCV (cv2) reads images in BGR (Blue, Green, Red) format by default, 
        # whereas the hand detection model from MediaPipe (mp.solutions.hands.Hands()) expects the image to be in RGB format (Red, Green, Blue).
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        
        # Update the window display with current game state and get the button of Menu
        update_window(Window, Lines_color, Lines_color_2, Lines_color_red,Lines_color_pink, Width, Square, Small_Square, Red_rose_small, Pink_rose_small, Red_rose, Pink_rose, small_boards, main_board, box, turn, text_x, text_y,  text_width, text_height, text1_text, Play_butt_text, Play_butt_y, pos_v, Bg)          
       
        # The Client (Them) plays
        if turn == 1:
            data = s.recv(1024).decode()
            if data.startswith("UTTT/1.0 PLAY"):
                time_sec = time.time()
                waiting_time = 0
                waiting = True
                data = data.split("\n")
                _, _, position, hash = data[0].split()
                big_slot, small_slot = int(position[0]), int(position[1])
                x, y = calculate_position_received(big_slot, small_slot)

                #set the location of the Client
                
                if set_locations(small_boards, main_board, x, y, turn, box):
                    
                    # Uupdate the hash
                    my_hash =haching_function(text_state_game(small_boards))
                    # send it 
                    s.sendall(f"UTTT/1.0 NEW_STATE {my_hash}\n".encode())
                    # Get the time, make a while loop waiting fo the ACk 

                    
                    while waiting == True :
                        data = s.recv(1024).decode()
                        waiting_time = abs(time_sec - time.time())
                        if data.startswith("UTTT/1.0 ACK"):
                            waiting = False
                        elif data.startswith("UTTT/1.0 404 STATE_PLAY"):
                            my_hash = haching_function(text_state_game(small_boards))
                            s.sendall(f"UTTT/1.0 NEW_STATE {my_hash}\n".encode())
                            
                        elif waiting_time > time_out or data.startswith("UTTT/1.0 FATAL_ERROR\n"):
                            if waiting_time > time_out :
                                s.sendall(f"UTTT/1.0 406 FATAL_ERROR\n".encode())
                            game_not_over = False
                            waiting = False
                            s.close()
                            Winner(2,Window)
                    # Check if the game has ended after this move
                    # Check for small wins
                    check_game(small_boards, main_board,turn)
                    
                    # Get possible moves on the newly selected small board
                    box = get_possible_moves(small_boards,x, y, main_board)

                    # Check for a win on the main board after this move
                    new_winner = Check_Big_Board(main_board, turn)

                    # If there are no boxes left to play but the big board has no winner
                    if box == [] and new_winner == 0: 
                        s.sendall("UTTT/1.0 WIN\n".encode())
                        time_sec = time.time()
                        waiting_time = 0
                        waiting = True
                        while waiting:
                            waiting_time = abs(time_sec - time.time())
                            data = s.recv(1024).decode()
                            if data.startswith("UTTT/1.0 END"):
                                game_not_over = False
                                s.close()
                                Winner(new_winner,Window)
                            elif waiting_time > time_out or data.startswith("UTTT/1.0 406 FATAL_ERROR\n"):
                                if waiting_time > time_out :
                                    s.sendall(f"UTTT/1.0 406 FATAL_ERROR\n".encode())
                                game_not_over = False
                                waiting = False
                                s.close()
                                Winner(2,Window)
                        
                    elif new_winner != 0:
                        time_sec = time.time()
                        waiting_time = 0
                        waiting = True
                        game_not_over = False
                        if new_winner == -1:
                            text = "HOST"
                        if new_winner == 1:
                            text ="GUEST"
                        if new_winner == 2:
                            text = ""
                        while waiting :
                            s.sendall(f"UTTT/1.0 WIN {text}\n".encode())
                            waiting_time = abs(time_sec - time.time())
                            data = s.recv(1024).decode()
                            if data.startswith("UTTT/1.0 END"):
                                game_not_over = False
                                s.close()
                                Winner(new_winner,Window)
                            elif waiting_time > time_out or data.startswith("UTTT/1.0 FATAL_ERROR\n"):
                                if waiting_time > time_out :
                                    s.sendall(f"UTTT/1.0 406 FATAL_ERROR\n".encode())
                                game_not_over = False
                                waiting = False
                                s.close()
                                Winner(2,Window)


                                            
                    # Switch turns
                    turn = turn * (-1)
                else:
                    s.sendall("UTTT/1.0 405 BAD_REQUEST\n".encode())
                    s.close()
                    Winner(2,Window)  
                        
            elif data.startswith("UTTT/1.0 END"):
                game_not_over = False
                s.close()
                Winner(2,Window)      
            else :
                print("wtf is this error")
                s.close()
                quit()
                        
        # The Host(us) plays
        elif turn == -1 : 
            if hands:
                hand = hands[0]
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    
                    if id == 0:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                        hand_y = screen_height/frame_height*y

                    if id == 4:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y
                    
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                        finger2_x = screen_width/frame_width*x
                        finger2_y = screen_height/frame_height*y

                    if id == 12:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                        finger3_x = screen_width/frame_width*x
                        finger3_y = screen_height/frame_height*y

                    if id == 16:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                        finger4_x = screen_width/frame_width*x
                        finger4_y = screen_height/frame_height*y
                    if id == 20:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                        finger5_x = screen_width/frame_width*x
                        finger5_y = screen_height/frame_height*y
                        print(2*hand_y - finger5_y-finger2_y)
                        if abs(hand_y - finger4_y+hand_y - finger2_y+hand_y - finger3_y+hand_y - finger5_y) < 260:
                            x,y,z,a=pos_v
                            if set_locations(small_boards, main_board, (x+5)//(Small_Square), (y+5)//(Small_Square), turn, box):
                                # Sent location of where you put the board
                                bs, ss = calculate_position_to_send((x+5)//(Small_Square), (y+5)//(Small_Square))
                                s.sendall(f"UTTT/1.0 PLAY {bs}{ss} {my_hash}\n".encode())
                                
                                # Get the time, make a while loop waiting fo the ACk 
                                time_sec = time.time()
                                waiting_time = 0
                                waiting = True
                                error = 0
                                while waiting == True :
                                    data = s.recv(1024).decode()
                                    waiting_time = abs(time_sec - time.time())
                                    
                                    if waiting_time > time_out or error == 2:
                                        s.sendall(f"UTTT/1.0 406 FATAL_ERROR\n".encode())
                                        game_not_over = False
                                        s.close()
                                        Winner(2,Window)
                                        
                                    elif data.startswith("UTTT/1.0 NEW_STATE"):
                                        
                                        my_hash = haching_function(text_state_game(small_boards))
                                        data = data.split("\n")
                                        _, _, hash = data[0].split()
                                        if hash == my_hash :
                                            s.sendall("UTTT/1.0 ACK\n".encode())
                                            waiting = False
                                        else: 
                                            error += 1
                                            s.sendall(f"UTTT/1.0 404 STATE_PLAY {position} {my_hash}\n".encode())
                                    
                                    elif  data.startswith("UTTT/1.0 405 BAD_REQUEST"):
                                        s.sendall(f"UTTT/1.0 PLAY {bs}{ss} {my_hash}\n".encode())
                                    
                                        

                                # Check if the game has ended after this move
                                # Check for small wins
                                check_game(small_boards, main_board,turn)
                                # Get possible moves on the newly selected small board
                                box = get_possible_moves(small_boards,(x+5)//(Small_Square), (y+5)//(Small_Square), main_board)

                                # Check for a win on the main board after this move
                                new_winner = Check_Big_Board(main_board, turn)

                                # If there are no boxes left to play but the big board has no winner
                                if box == [] and new_winner == 0: 
                                    data = s.recv(1024).decode()
                                    if data.startswith("UTTT/1.0 WIN\n"):
                                        s.sendall("UTTT/1.0 END".encode())
                                        game_not_over = False
                                        s.close()
                                        Winner(new_winner,Window)
                                    
                                    else : 
                                        s.sendall(f"UTTT/1.0 406 FATAL_ERROR\n".encode())
                                        game_not_over = False
                                        s.close()
                                        with open('Start.py')as new:
                                            exec(new.read())
                                    
                                elif new_winner != 0:
                                    time_sec = time.time()
                                    waiting_time = 0
                                    waiting = True
                                    game_not_over = False
                                    if new_winner == -1:
                                        text = "HOST"
                                    elif new_winner == 1:
                                        text ="GUEST"
                                    data = s.recv(1024).decode()
                                    if data.startswith("UTTT/1.0 WIN"):
                                        data = data.split("\n")
                                        data = data[0].split()
                                        if len(data)==3:
                                            _, _, name_winner = data
                                            if text == name_winner :
                                                s.sendall("UTTT/1.0 END".encode())
                                                game_not_over = False
                                                s.close()
                                                Winner(new_winner,Window)
                                                
                                        elif new_winner == 2:
                                            s.sendall("UTTT/1.0 END".encode())
                                            game_not_over = False
                                            s.close()
                                            Winner(new_winner,Window)
                                    s.sendall("UTTT/1.0 FATAL_ERROR\n".encode())
                                    game_not_over = False
                                    s.close()
                                    with open('Start.py')as new:
                                        exec(new.read())            
                                # Switch turns
                                turn = turn * (-1)
                        elif math.sqrt((thumb_x-finger2_x)**2+(thumb_y-finger2_y)**2)<100:
                            pos_v = go_left(pos_v)
                    
                        elif math.sqrt((thumb_x-finger3_x)**2+(thumb_y-finger3_y)**2)<100:
                            pos_v =go_right(pos_v)

                        elif math.sqrt((thumb_x-finger4_x)**2+(thumb_y-finger4_y)**2)<100:
                            pos_v =go_up(pos_v)
                        
                        elif math.sqrt((thumb_x-finger5_x)**2+(thumb_y-finger5_y)**2)<100:
                            pos_v =go_down(pos_v)

                        elif abs(hand_y - finger3_y+hand_y - finger4_y+hand_y - finger5_y) < 350 and abs(hand_y - finger2_y) > 300:
                            pos_v = place(pos_v,box)
                        elif abs(2*hand_y-finger3_y-finger4_y)<200  and abs(2*hand_y - finger5_y-finger2_y)>500:
                            game_not_over = False
                            print("Let's play again")
                            s.sendall("UTTT/1.0 END\n".encode())# Tell the other one you are leaving 
                            s.close()
                            with open('Start.py')as new:
                                exec(new.read()) 
        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)
        pygame.display.update()    