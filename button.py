import pygame

class Button:
    def __init__(self, surface, x, y, width, height):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def makeButton(self, color, button_alpha : int = 255):
        self.button = pygame.Surface((self.width, self.height))
        self.color = color
        self.button_alpha = button_alpha

        self.mouseOver = self.checkMouse()

        if not self.mouseOver:
            self.button.fill(color)
            self.button.set_alpha(self.button_alpha)
            self.surface.blit(self.button, (self.x, self.y))

    def buttonAction(self, action_color, action_alpha : int = 255, action = None):
        self.action_color = action_color
        self.action_alpha = action_alpha
        self.action = action

        self.mouseOver = self.checkMouse()

        if self.mouseOver:
            self.button = pygame.Surface((self.width + 10, self.height + 10))
            self.button.fill(self.action_color)
            self.button.set_alpha(self.action_alpha)
            self.surface.blit(self.button, (self.x - 5, self.y - 5))

            if self.click[0] and self.action != None:
                self.action()

    def textHandler(self, text, text_color, font = 'Arial', font_size = 24):
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = font
        self.loadFont = pygame.font.SysFont(font, self.font_size)

        self.text_surface = self.loadFont.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (round(self.x + (self.width / 2)), round(self.y + (self.height / 2)))
        
        self.surface.blit(self.text_surface, self.text_rect)

    def checkMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.mouseOver = False

        if self.x + self.width > self.mouse_pos[0] > self.x and self.y + self.height > self.mouse_pos[1] > self.y:
            self.mouseOver = True
        
        return self.mouseOver

    def update(self):
        self.makeButton(self.color, self.button_alpha)
        self.buttonAction(self.action_color, self.action_alpha, self.action)
        self.textHandler(self.text, self.text_color, self.font, self.font_size)