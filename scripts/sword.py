from scripts.vfx import Vfx
import pygame
class Sword():
    def __init__(self,x,y,damage = 10):
        self.damage = damage#damage of the sword
        self.arc = None#the arc of the sword
        self.arcDone = True#is the arc done
        self.hitbox = pygame.Rect(x,y,20,40)#hitbox of the sword

    def update(self,x,y,surface,scroll,enemies):#update the sword
        
        
        if self.arc is not None:#if the arc is not none
            self.hitbox.x = (self.arc.x)#set the hitbox to the arc
            self.hitbox.y = (self.arc.y)#set the hitbox to the arc
            if self.arc.flip:#if the arc is flipped
                self.hitbox.x += 20#move the hitbox to the left
            for enemy in enemies:#for each enemy
                if enemy.rect.colliderect(self.hitbox):#if the enemy is colliding with the hitbox
                    enemy.takeDamage(self.damage)#damage the enemy
            self.arcDone = self.arc.update(x,y,surface,scroll)#update the arc
            if self.arcDone:#if the arc is done
                self.arc = None#set the arc to none
            
                
      
    def newBezeirArc(self,x,y,flip,direction):#create a new arc
        return Vfx.BezierArc((0, 0), (0, 200), (200, 100), (21, 244, 238), 5,direction,x,y-16,revealSpeed = 160,flip=flip)#create a new arc
