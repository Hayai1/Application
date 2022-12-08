import pygame
class Cursor():
    def __init__(self):
        self.rect = pygame.Rect(0,0,8,8)
        self.click = False
    def update(self):
        mx,my=pygame.mouse.get_pos()
        self.rect.x = mx
        self.rect.y = my

            
