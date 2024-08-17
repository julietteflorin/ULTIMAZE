# Import necessary modules
import pygame
import os
import UTTT_Guest_As_Human
import UTTT_Host_As_Human
import UTTT_Guest_AI
import UTTT_Host_AI

# Function to create a button
def create_button(button_text, x, y, width, height):
    """This creats butons"""
    button_rect = pygame.Rect(x, y, width, height)
    text_rect = button_text.get_rect(center=button_rect.center)
    return button_rect, text_rect

def online_menu(guest_host):
    #Initialise pygame
    pygame.init()
    gameIcon = pygame.image.load(os.path.join("Images", "logo_ultimaze.jpg"))
    pygame.display.set_icon(gameIcon)

    # Set screen dimensions
    screen_width = 900
    screen_height = 620
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu Ultimate Tic Tac Toe")

    # Colors

    black = (0, 0, 0)
    white = (255, 255, 255)

    #Image
    if guest_host == "GUEST" :
        menu_image = pygame.image.load(os.path.join("Images", "Menu_online_guest.png"))
    else :
        menu_image = pygame.image.load(os.path.join("Images", "Menu_online_host.png"))

    # Font for text
    font = pygame.font.Font('Precious.ttf', 30)

    # Button dimensions
    button_width = 150
    button_height = 50

    # Button positions
    button1_x = screen_width // 2 - button_width // 2
    button2_y = screen_height // 2 - button_height
    button1_y = button2_y - button_height - 20
    button_menu_x = button1_x
    button_menu_y = screen_height - button_height -20

    # Button text
    button1_text = font.render(u"Human", True, black)# Just send position il recoit qui commence 
    button2_text = font.render(u"AI", True, black)# Le host écoute et choisit qui commence 
    button_menu_text = font.render(u"Menu", True, black)
    

    # Create button rects and text rects
    button1_rect, button1_text_rect = create_button(
        button1_text, button1_x, button1_y, button_width, button_height, 
    )
    button2_rect, button2_text_rect = create_button(
        button2_text, button1_x, button2_y, button_width, button_height, 
    )
    button_menu_rect, button_menu_text_rect = create_button(
        button_menu_text, button_menu_x, button_menu_y, button_width, button_height, 
    )
    # Show all of the screen
    running = True
    while running:
        # If somethings happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check for mouse clicks on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button1_rect.collidepoint(mouse_pos):
                    if guest_host == "GUEST":
                        running = False
                        UTTT_Guest_As_Human.main()
                    else :
                        running = False
                        UTTT_Host_As_Human.main()
                if button2_rect.collidepoint(mouse_pos):
                    if guest_host == "GUEST":
                        running = False
                        UTTT_Guest_AI.main()
                    else :
                        running = False
                        UTTT_Host_AI.main()
                if button_menu_rect.collidepoint(mouse_pos):
                    running = False
                    with open('Start.py')as new:
                        exec(new.read())
                    
        # Fill screen with background color
        screen.blit(menu_image,(0,0))

        # Draw buttons and color according to button to click
        pygame.draw.rect(screen, button1_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or white, button1_rect)
        pygame.draw.rect(screen, button2_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or white, button2_rect)
        pygame.draw.rect(screen, button_menu_rect.collidepoint(pygame.mouse.get_pos()) and white or (255,166,190), button_menu_rect)
        # Show the buttons
        screen.blit(button1_text, button1_text_rect)
        screen.blit(button2_text, button2_text_rect)
        screen.blit(button_menu_text, button_menu_text_rect)

        pygame.display.update()

    pygame.quit()

