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

    def update(self,surface,scroll):
        if self.arc is not None:
            self.arcDone = self.arc.update(surface,scroll)
            if self.arcDone:
                self.arc = None
                
                
      
    def newBezeirArc(self,x,y,flip):
        return Vfx.BezierArc((0, 0), (0, 200), (200, 100), (21, 244, 238), 5,x,y-16,flip=flip)
