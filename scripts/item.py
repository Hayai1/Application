import pygame
class Item:
    def __init__(self,thumbnailPath,useImgPath):
        self.thumbnailImg = self.getImg(thumbnailPath)
        self.useImg = self.getImg(useImgPath)
    def getImg(self,path):
        if path == None:
            return None
        else:
            return pygame.image.load(path)
    def draw():
        pass
    def update():
        pass