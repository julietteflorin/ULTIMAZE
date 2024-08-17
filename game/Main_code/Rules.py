import pygame
import os
from Main_code.Rulesmore import detailes_rules
def create_button(button_text, x, y, width, height):
    """This creats butons"""
    button_rect = pygame.Rect(x, y, width, height)
    text_rect = button_text.get_rect(center=button_rect.center)
    return button_rect, text_rect

def main_rules():
    screen_width = 964
    screen_height = 641
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rules Ultimaze")
    gameIcon = pygame.image.load(os.path.join("Images", "logo_ultimaze.jpg"))
    pygame.display.set_icon(gameIcon)
    
    
    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    #Image
    menu_image = pygame.image.load(os.path.join("Images", "Game_rules.png"))
    # Font for text
    font = pygame.font.Font('Precious.ttf', 40)
    
    
    # Button
    button_width = 300
    button_height = 60
    
    button_x = 163
    button_y = 570
    button2_x = button_x
    button2_y = screen_height - button_y - button_height
    
    button_text= font.render(u"Menu", True, black)
    button2_text= font.render(u"More Details", True, black)
    
    button_rect, button_text_rect = create_button(
        button_text, button_x, button_y, button_width, button_height, 
    )
    button2_rect, button2_text_rect = create_button(
        button2_text, button2_x, button2_y, button_width, button_height, 
    )
    running = True
    while running:
        # If somethings happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check for mouse clicks on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    running = False
                    with open('Start.py')as new:
                        exec(new.read())
                if button2_rect.collidepoint(mouse_pos):
                    running = False
                    detailes_rules()
                        
        screen.blit(menu_image,(0,0))
        # Draw button and color according to button to click
        pygame.draw.rect(screen, button_rect.collidepoint(pygame.mouse.get_pos()) and white or (255,166,190), button_rect)
        pygame.draw.rect(screen, button2_rect.collidepoint(pygame.mouse.get_pos()) and white or (255,166,190), button2_rect)
        # Show the buttons
        screen.blit(button_text, button_text_rect)
        screen.blit(button2_text, button2_text_rect)
        pygame.display.update()
    pygame.quit()