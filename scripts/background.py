import pygame
class BackGround():
    def __init__(self,imgpath):
        self.img = pygame.image.load(imgpath)
    def draw(self,surface,scroll):
        surface.blit(self.img,scroll)
    def update(self,screen, scroll):
        screen.blit(self.img,[(scroll[0]-32)/40,(scroll[1]-32)/40])