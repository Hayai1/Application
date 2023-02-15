
import pygame, time
from scripts.ai import Ai
from scripts.character import Character

class Enemy(Character):
    def __init__(self,x, y, width, height,graph,imgPath,velocity=[],acceleration=[0,0],target=None,surf=None,camera=None,collisionRects=None):
        self.target=target
        self.surf=surf
        self.camera=camera
        self.collisionRects=collisionRects
        self.graph = graph
        self.img = pygame.image.load(imgPath)
        self.img.set_colorkey((0,0,0))
        super().__init__(x, y, width, height,velocity,acceleration)
        self.ai = Ai(self.rect, target,graph)
    
    def getAnimations(self):
        return NotImplementedError

    def draw(self,screen,scroll):
        screen.blit(pygame.transform.flip(self.img,self.flip,False), (self.rect.x - scroll[0],self.rect.y - scroll[1]))
      
    def update(self):  
        left, right, jump = self.ai.getDirection(self.airTimer)
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right
        if jump:
            self.playerJump()        
    
        #-------------------------------------------------------------#
        movement = self.move(self.collisionRects)#call the move function
        self.draw(self.surf,self.camera.scroll)#draw the enemy
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        
           