from scripts.item import Item
from scripts.vfx import Vfx
import random,pygame
class Sword(Item):
    def __init__(self,thumbnailPath,useImgPath,damage = 10, attackSpeed = 1):
        Item.__init__(self,thumbnailPath,useImgPath)
        self.damage = damage
        self.attackSpeed = attackSpeed
        self.arc = None
        self.arcDone = True
        self.slashSurface = pygame.Surface((100,100))
        self.slashSurface.set_colorkey((0,0,0))
    def newArc(self):
        rad = random.uniform(1, 1.5)
        curveRate = random.uniform(75, 200)
        arcStretch = random.uniform(100, 200)
        return Vfx.Arc(pos=[50,50], radius=rad, spacing=1.13, startAngle=-0.19, 
                       speed=1, curveRate=curveRate, scale=0.5, start=1, end=1, 
                       duration=0.2, color=(21, 244, 238), fade=0.7, arcStretch=arcStretch, 
                       widthDecay=2, motion=100, decay=['up', 300], angleWidth=0.5
                       )
    def swing(self):
        if self.arcDone:
            self.arc = self.newArc()
            self.arcDone = False
        
    def update(self):
        self.slashSurface.fill((0,0,0))
        

        if self.arc is not None:
            self.ArcDone = self.arc.update()
            self.arc.render(self.slashSurface)
            if self.ArcDone:
                self.arc = None
        else:
            self.arcDone = True