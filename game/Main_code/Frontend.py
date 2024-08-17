import pygame
import os


def Draw_pieces(Win, Red_rose_small, Pink_rose_small,Red_rose, Pink_rose, Small_Square, Square, small_board, main_board):
    """Draw the pices where the players are on the board"""
    for x1 in range(len(small_board)):
        for y1 in range(len(small_board)):
            if small_board[y1][x1] == -1 and main_board[y1//3][x1//3] == 0:
                Win.blit(Pink_rose_small, (x1*Small_Square, y1*Small_Square))
            if small_board[y1][x1] == 1 and main_board[y1//3][x1//3] == 0:
                Win.blit(Red_rose_small, (x1*Small_Square, y1*Small_Square))

def draw_big_pieces(Win, big_board, Square, Pink_rose, Red_rose):
    """Draw the pieces on the big tic tac toe"""
    for x2 in range(len(big_board)):
        for y2 in range(len(big_board)):
            if big_board[y2][x2] == -1:
                Win.blit(Pink_rose, (x2*Square, y2*Square))

            if big_board[y2][x2] == 1:
                Win.blit(Red_rose, (x2*Square, y2*Square))
            # If there is no winner on the box

def combination(box, move, ab):
    """This checks if there is one possible move in a little tic tac toe and returns true if there is"""
    move_1 = move*3
    move_2 = ab*3
    for i in range(3):
        for j in range(3):
            if [move_1 + i, move_2 + j] in box:
                # Found a combination
                return True
    return False

def draw_board(Win, Lines_color, Lines_color_2, Lines_color_red,Lines_color_pink, Width, Square, Small_Square, player,box):
    """Draw the board"""
    Height = Width
    Color_small_line = Lines_color_2
    thickness = 4
    #Small Boards
    for move in range(0,3):  
        for ab in range(0,3):
            if box == None or combination(box, move, ab) == True:
                if player == 1 :
                    Color_small_line = Lines_color_red
                    thickness = 10
                else :
                    Color_small_line = Lines_color_pink
                    thickness = 10
            else :
                Color_small_line = Lines_color_2
                thickness = 2
            for x in range(1,3): #Horizontal lines
                pygame.draw.line(Win, Color_small_line, (Square*move, (x*Small_Square) + ab*Square), ((Square) + Square*move,(x*Small_Square) + ab*Square), thickness)
            for bc in range(0,2): # Vertical lines
                pygame.draw.line(Win, Color_small_line, (Small_Square + bc*Small_Square + move*Square, ab*Square), (Small_Square + bc*Small_Square + move*Square, (Square) + ab*Square), thickness)

    #Big Board
    for i in range(0,4): #Draw horizontal lines
        pygame.draw.line(Win, Lines_color, (0, Square*i), (Width, Square*i), 5)

    for j in range(0,4): #Draw vertical lines
        pygame.draw.line(Win, Lines_color, (Square*j, 0), (Square*j, Height), 5)
    




def Winner(player, Window):
    """If there is a winner this goes showes the new interface"""
    # Define screen dimensions
    # Define background
    Width, Height = 900, 620


    # Load image assets for game pieces
    Red_rose_winner = pygame.image.load(os.path.join("Images", "Red_rose_winner.png"))
    
    Pink_rose_winner = pygame.image.load(os.path.join("Images", "Pink_rose_winner.png"))
    No_winner = pygame.image.load(os.path.join("Images", "No_winner.png"))
    
    Window = pygame.display.set_mode((Width, Height))
    run = True
    pygame.display.set_caption("Winner of the Ultimate Tic Tac Toe")
    
    clock = pygame.time.Clock()  # Used to control frame rate
    FPS = 120  # Frames per second
    
    # Font for text
    font = pygame.font.Font(None, 40)

    # Button dimensions
    button_width = 300
    button_height = 50
    # Button positions
    button_x = Width // 2 - button_width // 2
    button_y = Height - button_height*2
    # Button text
    button1_text = font.render(u"Play again", True, (0,0,0))
    
    # Create button rects and text rects
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button_text_rect = button1_text.get_rect(center=button_rect.center)
    while run:
        clock.tick(FPS)


        if player == -1:
            #print("Player with pink rose wins")
            Window.blit(Pink_rose_winner,(0,0) )
            
        elif player == 1:
            #print("Player with red rose wins")
            Window.blit(Red_rose_winner,(0,0))
            
        elif player == 2:
            #print("no one wins")
            Window.blit(No_winner,(0,0))
        pygame.draw.rect(Window, button_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or (255,255,255), button_rect)
        Window.blit(button1_text, button_text_rect)
        pygame.display.update()
        
        # Get events
        
        for event in pygame.event.get():
        # Quit the game
            if event.type == pygame.QUIT:
                    quit()
            # Check for mouse clicks on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    run = False
                    print("Let's play again")
                    with open(os.path.dirname(__file__) + '/../Start.py')as new:
                        exec(new.read())
                        
                        
def update_window_nocam(Win, Lines_color, Lines_color_2, Lines_color_red,Lines_color_pink, Width, Square, Small_Square, Red_rose_small, Pink_rose_small, Red_rose, Pink_rose, small_board, main_board, box, player,text_x, text_y, text_width, text_height, text1_text, Play_butt_text, Play_butt_y):
    """
    Fills the background, draws game pieces, board lines, and big pieces, then updates the display.
    """
    if player == 1:
        player_im = Red_rose_small
    else :
        player_im = Pink_rose_small
    fond_image = pygame.image.load(os.path.join("Images", "fond_game.png"))
    Win.blit(fond_image,(0,0))
    Draw_pieces(Win, Red_rose_small, Pink_rose_small, Red_rose, Pink_rose, Small_Square, Square, small_board, main_board)
    draw_board(Win, Lines_color, Lines_color_2, Lines_color_red,Lines_color_pink, Width, Square, Small_Square, player, box)
    draw_big_pieces(Win, main_board, Square, Pink_rose, Red_rose)
    
     #Text for who plays
    # Create text rects and Text of who plays rects
    text_rect = pygame.Rect(text_x, text_y, text_width, text_height)
    text_text_rect = text1_text.get_rect(center=text_rect.center)
    pygame.draw.rect(Win, (255,255,255), text_rect)

    # Button to go back to the Menu
    # Create text rects 
    play_rect = pygame.Rect(text_x, Play_butt_y, text_width, text_height)
    Play_text_rect = Play_butt_text.get_rect(center=play_rect.center)
    pygame.draw.rect(Win, play_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or (255,255,255), play_rect)
    
    # display
    Win.blit(player_im, ((text_x + text_width//2) - Small_Square//2 , text_y + text_height))
    Win.blit(text1_text, text_text_rect)
    Win.blit(Play_butt_text, Play_text_rect)
    
    pygame.display.update()

    return play_rect

# Function to update the game window display with hand detection
def update_window(Win, Lines_color, Lines_color_2, Lines_color_red,Lines_color_pink, Width, Square, Small_Square, Red_rose_small, Pink_rose_small, Red_rose, Pink_rose, board, big_board, box, player,text_x, text_y, text_width, text_height, text1_text, Play_butt_text, Play_butt_y, pos_v, Bg):
    """
    Creates the background, draws game pieces, board lines, the buttons and big pieces, then updates the display.
    """
    # What image to display according to who is playing
    if player == 1:
        player_im = Red_rose_small
    else :
        player_im = Pink_rose_small
        
    fond_image = pygame.image.load(os.path.join("Images", "fond_game.png"))
    Win.blit(fond_image,(0,0))

    Draw_pieces(Win, Red_rose_small, Pink_rose_small, Red_rose, Pink_rose, Small_Square, Square, board, big_board)
    draw_board(Win, Lines_color, Lines_color_2, Lines_color_red,Lines_color_pink, Width, Square, Small_Square, player, box)
    draw_big_pieces(Win, big_board, Square, Pink_rose, Red_rose)
    
    # Create text rects and text of who plays
    text_rect = pygame.Rect(text_x, text_y, text_width, text_height)
    text_text_rect = text1_text.get_rect(center=text_rect.center)
    pygame.draw.rect(Win, (255,255,255), text_rect)
    
    # Create the button to go back to the Menu
    play_button = pygame.Rect(text_x, Play_butt_y, text_width, text_height)
    Play_text_rect = Play_butt_text.get_rect(center=play_button.center)
    pygame.draw.rect(Win, play_button.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or (255,255,255), play_button)
    
    play_rect = pygame.Rect(pos_v)
    pygame.draw.rect(Win, (128, 0, 128), play_rect)
    
    # display all of it

    Win.blit(player_im, ((text_x + text_width//2) - Small_Square//2 , text_y + text_height))
    Win.blit(text1_text, text_text_rect)
    Win.blit(Play_butt_text, Play_text_rect)
   