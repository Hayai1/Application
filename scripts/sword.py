from scripts.item import Item
from scripts.vfx import Vfx
import random,pygame
class Sword(Item):
    def __init__(self,x,y,thumbnailPath,useImgPath,damage = 10, attackSpeed = 1):
        Item.__init__(self,thumbnailPath,useImgPath)
        self.damage = damage
        self.attackSpeed = attackSpeed
        self.arc = None
        self.arcDone = True
        self.hitbox = pygame.Rect(x,y,20,40)

    def update(self,x,y,surface,scroll):
        
        
        if self.arc is not None:
            self.hitbox.x = (self.arc.x)-scroll[0]
            self.hitbox.y = (self.arc.y)-scroll[1]
            if self.arc.flip:
                self.hitbox.x += 20

            #pygame.draw.rect(surface, (255,0,0), self.hitbox)
            self.arcDone = self.arc.update(surface,scroll)
            if self.arcDone:
                self.arc = None
            
                
      
    def newBezeirArc(self,x,y,flip):
        return Vfx.BezierArc((0, 0), (0, 200), (200, 100), (21, 244, 238), 5,x,y-16,flip=flip)
