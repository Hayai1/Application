
import pygame, time
from scripts.ai import Ai
from scripts.character import Character
from scripts.animations import Animations
class Enemy(Character):
    def __init__(self,x, y, width, height,graph,imgPath,velocity=[],acceleration=[0,0],target=None,surf=None,camera=None,collisionRects=None):
        self.target=target
        self.surf=surf
        self.camera=camera
        self.collisionRects=collisionRects
        self.graph = graph
        self.attackTimer = 100
        self.img = pygame.image.load(imgPath)
        self.img.set_colorkey((0,0,0))
        super().__init__(x, y, width, height,velocity,acceleration)
        self.ai = Ai(self.rect, target,graph)
    
    def getAnimations(self):
        animations = Animations('assets/enemyAnimations')
        animations.getAnimation('run',[4,4,4,4,4,4,4])
        animations.getAnimation('idle',[6,6,6,6,6,6,6,6])
        animations.getAnimation('attack',[4,4,4,20,3,4,4,4])
        return animations
    def changeAnimationState(self,movement):
        self.attackTimer -= 1 
        if self.attackTimer < 0 and self.x - self.target.x < 50 and self.x - self.target.x > -50 and self.y - self.target.y < 50 and self.y - self.target.y > -50:
            self.animations.changeState('attack')
            if self.animations.getCurrentImg() == 'attack7':self.attackTimer = 100
        else:
            if movement[0] == 0:self.animations.changeState('idle')
            if movement[0] > 0:self.animations.changeState('run')
            if movement[0] < 0:self.animations.changeState('run')

    def setDirectionToMove(self):
        ChangeInleft, ChangeInright, jump = self.ai.getDirection(self.airTimer)
        if ChangeInleft is not None:self.left = ChangeInleft
        if ChangeInright is not None:self.right = ChangeInright
        if jump:self.playerJump()        
    
    def update(self):  
        self.setDirectionToMove()
        #-------------------------------------------------------------#
        self.x = self.rect.x 
        self.y = self.rect.y
        movement = self.move(self.collisionRects)#call the move function
        self.changeAnimationState(movement)
        self.draw(self.surf,self.camera.scroll,self.animations.getImg())#draw the enemy
  
        
           