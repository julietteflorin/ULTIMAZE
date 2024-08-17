# Import necessary modules
import pygame
from pygame.locals import *
import os

from Main_code.Rules import main_rules
from Main_code.Menu_online import online_menu
from Main_code.Menu_Local import local_menu

# Function to create a button
def create_button(button_text, x, y, width, height):
    """This creats butons"""
    button_rect = pygame.Rect(x, y, width, height)
    text_rect = button_text.get_rect(center=button_rect.center)
    return button_rect, text_rect

def main():
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
    menu_image = pygame.image.load(os.path.join("Images", "font_rose.png"))

    # Font for text
    font = pygame.font.Font('Precious.ttf', 40)
    # Button dimensions
    button_width = 300
    button_height = 50

    # Button positions
    button1_x = screen_width // 2 - button_width // 2
    button2_y = screen_height // 2 - button_height
    button1_y = button2_y - button_height - 20
    button3_y = button2_y + button_height + 20
    button_rules_x = screen_width // 2 - button_width - button_width//4
    button_rules_y = button2_y

    # Button text
    button1_text = font.render("Local", True, black)
    button2_text = font.render("Join Server", True, black)
    button3_text = font.render("Host Server", True, black)
    button_rules_text = font.render("Rules", True, black)
    

    # Create button rects and text rects
    button1_rect, button1_text_rect = create_button(
        button1_text, button1_x, button1_y, button_width, button_height, 
    )
    button2_rect, button2_text_rect = create_button(
        button2_text, button1_x, button2_y, button_width, button_height, 
    )
    button3_rect, button3_text_rect = create_button(
        button3_text, button1_x, button3_y, button_width, button_height, 
    )

    button_rules_rect, button_rules_text_rect = create_button(
        button_rules_text, button_rules_x, button_rules_y, button_width//2, button_height, 
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
                    running = False
                    local_menu()
                    
                if button2_rect.collidepoint(mouse_pos):
                    running = False
                    online_menu("GUEST")
                    
                if button3_rect.collidepoint(mouse_pos):
                    running = False
                    online_menu("HOST")
                    
                if button_rules_rect.collidepoint(mouse_pos):
                    running = False
                    main_rules()
                    
        # Fill screen with background color
        screen.blit(menu_image,(0,0))

        # Draw buttons and color according to button to click
        pygame.draw.rect(screen, button1_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or white, button1_rect)
        pygame.draw.rect(screen, button2_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or white, button2_rect)
        pygame.draw.rect(screen, button3_rect.collidepoint(pygame.mouse.get_pos()) and (200, 200, 200) or white, button3_rect)
        pygame.draw.rect(screen, button_rules_rect.collidepoint(pygame.mouse.get_pos()) and white or (255,166,190), button_rules_rect)
        # Show the buttons
        screen.blit(button1_text, button1_text_rect)
        screen.blit(button2_text, button2_text_rect)
        screen.blit(button3_text, button3_text_rect)
        screen.blit(button_rules_text, button_rules_text_rect)

        pygame.display.update()

    pygame.quit()

