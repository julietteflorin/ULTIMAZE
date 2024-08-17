import cv2
import mediapipe as mp
import pyautogui
import pygame
import matplotlib.pyplot as plt
import math
import random
import os
# Import modules containing game logic and functionality
from Main_code.hand_det import Quit_game, go_left, go_right, go_down, go_up, place
from Main_code.Board import new_Board
from Main_code.Frontend import Winner, update_window
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
    
def main():
    """
    The main game loop that handles events, updates the game state, and renders the display.
    """
    # ¨Parameter of the camera 
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    frame_width, frame_height = (640,480)
    hand_y = 0
    # Create the game window and set caption
    Window = pygame.display.set_mode((Screen_width, Height))
    pygame.display.set_caption("Ultimate Tic Tac Toe against AI")
    clock = pygame.time.Clock()  # Used to control frame rate
    
    # Position of the first purple square that is a refrence to where you are going to play
    pos_v=(360,360,90,90)
    turn = random.choice([-1, 1])  # Randomly choose starting player

    # Game settings
    FPS = 60  # Frames per second
    game_not_over = True

    # Game board variables
    box = None  # Tracks the currently selected small board within the bigger board
    main_board = Game_Board.create_board()  # Create the main board
    small_boards = Game_Board.every_small_boards()  # Create all small boards within the main board
    
    # Font for text
    font = pygame.font.Font('Precious.ttf', 40)

    # Text and buttons
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
        # If you detect hands
        if hands:
            # Check only one hand and draw it
            hand = hands[0]
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                # The different fingers to detect and use
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
                # Lets take action according to the distance from each finger to the middle space
                if id == 20:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                    finger5_x = screen_width/frame_width*x
                    finger5_y = screen_height/frame_height*y
                    
                    if abs(hand_y - finger4_y+hand_y - finger2_y+hand_y - finger3_y+hand_y - finger5_y) < 260:
                        x,y,z,a=pos_v
                        # If you can play there you may check the game
                        if set_locations(small_boards, main_board,  (x+5)//(Small_Square) ,(y+5)//(Small_Square), turn, box):
                            # Check if the game has ended after this move
                            check_game(small_boards, main_board,turn)

                            # Get possible moves on the newly selected small board
                            box = get_possible_moves(small_boards,(x+5)//(Small_Square), (y+5)//(Small_Square), main_board)

                            # Check for a win on the main board after this move
                            new_winner = Check_Big_Board(main_board, turn)
                            
                            # If there are no boxes left to play but the big board has no winner
                            if box == [] and new_winner == 0:
                                new_winner = 2
                            if new_winner != 0:
                                game_not_over = False
                                Winner(new_winner,Window)
                                
                            # Switch turns
                            turn = turn*(-1)    

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
                        with open('Start.py')as new:
                            exec(new.read())



            # Handle events
            cv2.imshow('Virtual Mouse', frame)
            cv2.waitKey(1)
            pygame.display.update()
        # function that are called by the detection of movement and that make the 




    
    


    
   

        
        
       


