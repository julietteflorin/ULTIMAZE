import pygame
import os
def create_button(button_text, x, y, width, height):
    """This creats butons"""
    button_rect = pygame.Rect(x, y, width, height)
    text_rect = button_text.get_rect(center=button_rect.center)
    return button_rect, text_rect

def detailes_rules():
    screen_width = 900
    screen_height = 620
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rules Ultimaze")
    gameIcon = pygame.image.load(os.path.join("Images", "logo_ultimaze.jpg"))
    pygame.display.set_icon(gameIcon)
    
    
    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    #Image
    rule_1 = pygame.image.load(os.path.join("Images", "Rule_1.png"))
    rule_2 = pygame.image.load(os.path.join("Images", "Rule_2.png"))
    rule_3 = pygame.image.load(os.path.join("Images", "Rule_3.png"))
    rule_4 = pygame.image.load(os.path.join("Images", "Rule_4.png"))
    
    # Font for text
    font = pygame.font.Font('Precious.ttf', 30)
    
    
    # Button
    button_width = 200
    button_height = 40
    
    button_prev_x = 10
    button_prev_y = screen_height - button_height - 10
    
    button_next_x = screen_width - button_width -button_prev_x
    button_next_y = button_prev_y
    
    button_next= font.render(u"Next", True, black)
    button_prev = font.render(u"Previous", True, black)
    
    button_next_rect, button_next_text_rect = create_button(
        button_next, button_next_x, button_next_y, button_width, button_height, 
    )
    button_prev_rect, button_prev_text_rect = create_button(
        button_prev, button_prev_x, button_prev_y, button_width, button_height, 
    )
    image = rule_1
    running = True
    while running:
        # If somethings happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check for mouse clicks on buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_next_rect.collidepoint(mouse_pos):
                    if image == rule_1:
                        image = rule_2
                    elif image == rule_2:
                        image = rule_3
                    elif image == rule_3:
                        image = rule_4
                    elif image == rule_4:
                        running = False
                        with open('Start.py')as new:
                            exec(new.read())
                if button_prev_rect.collidepoint(mouse_pos):
                    if image == rule_1:
                        running = False
                        with open('Start_Rules.py')as new:
                            exec(new.read())
                    elif image == rule_2:
                        image = rule_1
                    elif image == rule_3:
                        image = rule_2
                    elif image == rule_4:
                        image = rule_3
                        
        screen.blit(image,(0,0))
        # Draw button and color according to button to click
        pygame.draw.rect(screen, button_next_rect.collidepoint(pygame.mouse.get_pos()) and white or (255,166,190), button_next_rect)
        screen.blit(button_next, button_next_text_rect)
        pygame.draw.rect(screen, button_prev_rect.collidepoint(pygame.mouse.get_pos()) and white or (255,166,190), button_prev_rect)
        screen.blit(button_prev, button_prev_text_rect)

        
        pygame.display.update()
    pygame.quit()