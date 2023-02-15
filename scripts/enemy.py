
import pygame, time
from scripts.ai import Ai
from scripts.character import Character
from scripts.sword import Sword
class Enemy(Character):
    def __init__(self,x, y, width, height,graph,imgPath,velocity=[],acceleration=[0,0],target=None,surf=None,camera=None,collisionRects=None):
        self.target=target
        self.surf=surf
        self.camera=camera
        self.collisionRects=collisionRects
        self.name ="enemy"
        self.graph = graph
        self.img = pygame.image.load(imgPath)
        self.img.set_colorkey((0,0,0))
        super().__init__(x, y, width, height,velocity,acceleration)
        self.ai = Ai(self.rect, target,graph)
        self.path = None
        self.nextNode = None   
        self.moving = False
        self.jumping = False
        self.nodePointer = 0
        self.frame = 0
        self.movingFrames = 0
        self.newPathTimer = 0
        self.weapons = {'sword' : Sword(x,y,None,None)}
        self.attackTimer = 0
        
        
        self.currentNode = self.graph.getNodeCloseTo(self)
    def getAnimations(self):
        return NotImplementedError

    
    def getAttackRange(self,player):
        if self.x - player.x < 50 and self.x - player.x > -50 and self.y - player.y < 50 and self.y - player.y > -50:
            return True
        return False 

    def draw(self,screen,scroll):
        screen.blit(pygame.transform.flip(self.img,self.flip,False), (self.rect.x - scroll[0],self.rect.y - scroll[1]))
    def attack(self):
        if self.getAttackRange(self.target):
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip)
    
      
    def update(self):
        self.attackTimer +=1
        if self.attackTimer >= 50:
            self.attack()
            self.attackTimer = 0 
        self.weapons['sword'].update(self.x,self.y,self.surf,self.camera.scroll)
        
        if True:
            left, right, jump = self.ai.getDirection(self.airTimer)
            if left is not None:
                self.left = left
            if right is not None:
                self.right = right
            if jump:
                self.playerJump()        
        else:
            self.moveUpdate()
        #-------------------------------------------------------------#
        if self.weapons['sword'].arc is not None:
            self.left = False
            self.right = False
        movement = self.move(self.collisionRects)#call the move function
        self.draw(self.surf,self.camera.scroll)#draw the enemy
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        
           