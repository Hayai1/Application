import pygame
class Item:
    def __init__(self,thumbnailPath,useImgPath):
        self.thumbnailImg = pygame.image.load(thumbnailPath)
        self.useImg = pygame.image.load(useImgPath)
    