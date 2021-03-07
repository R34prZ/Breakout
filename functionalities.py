import pygame

def play_sound(sound) -> None:
    """ This function plays the selected sound. """
    sound_file = pygame.mixer.Sound(sound)
    pygame.mixer.Sound.play(sound_file)

def blit_text(surface, text, x, y, color, center_x = False, center_y = False, screen_size : tuple = None, font = './fonts/FreePixel.ttf', font_size = 36):
    """ This function makes it easy to blit text on screen"""
    font = pygame.font.SysFont(font, font_size)
    text_surface = font.render(text, True, color)
    
    if center_x:
        x = screen_size[0]/2 - text_surface.get_width()/2
    if center_y:
        y = screen_size[1]/2 - text_surface.get_height()/2

    surface.blit(text_surface, (x, y))


def make_button(surface, x, y, width, height, action_color, color, action = None, color_alpha = 255, text : str = None, text_color : tuple = (0,0,0), font = './fonts/FreePixel.ttf'):
    """This function makes cool buttons in a easy ready-to use way."""
    button = pygame.Surface((width, height))
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    button.fill(color)
    surface.blit(button, (x, y))
    
    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        button.fill(action_color)
        button.set_alpha(color_alpha)
        surface.blit(button, (x, y))

        if click[0] and action != None:
            action()
    
    def textObjects(text, font):
        text_surface = font.render(text, True, text_color)
        return text_surface, text_surface.get_rect()

    my_font = pygame.font.SysFont(font, 32)
    text_surface, text_rect = textObjects(text, my_font)
    text_rect.center = (round(x + (width / 2)), round(y + (height / 2))) 
    surface.blit(text_surface, text_rect)
