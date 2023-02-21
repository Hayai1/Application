import pygame

class Camera:
    def __init__(self,target):
        self.true_scroll = [0,0]
        self.scroll = [0,0]
        self.target = target
    def set_target(self,target):
        self.target = target
    def update(self):
        self.true_scroll[0] += (self.target.rect.x-self.true_scroll[0]-152)/20 
        self.true_scroll[1] += (self.target.rect.y-self.true_scroll[1]-106)/20
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
