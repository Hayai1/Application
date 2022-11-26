from scripts.item import Item
from scripts.vfx import Vfx
import random,pygame
class Sword(Item):
    def __init__(self,thumbnailPath,useImgPath,damage = 10, attackSpeed = 1):
        Item.__init__(self,thumbnailPath,useImgPath)
        self.damage = damage
        self.attackSpeed = attackSpeed
        self.arc = None
        self.arcNotDone = False
        self.sword = pygame.surface.Surface((200,200))
        self.sword.set_colorkey((0,0,0))
    def newArc(self,x,y):
        rad = random.uniform(2, 3)
        curveRate = random.uniform(75, 200)
        arcStretch = random.uniform(100, 200)
        angleWidth = random.uniform(0.5,10)
        return Vfx.Arc(pos=[50,50], radius=rad, spacing=1.13, startAngle=-0.19, speed=1, curveRate=curveRate, scale=0.5, 
                   start=1, end=1, duration=0.5, color=(255, 0, 0), fade=0.7, 
                   arcStretch=arcStretch, widthDecay=2, motion=100, decay=['up', 200], angleWidth=0.5)
    def swing(self,x,y):
        if not self.arcNotDone:
            self.arc = self.newArc(x,y)
            self.arcDone = False
        
    def update(self,surf,camera):
        self.sword.fill((0,0,0))
        if self.arc is not None:
            self.ArcNotDone = self.arc.update()
            self.arc.render(self.sword)
            if not self.ArcNotDone:
                self.arc = None
        else:
            self.arcNotDone = False