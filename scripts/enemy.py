
import pygame, time
from scripts.ai import Ai
from scripts.character import Character
from scripts.animations import Animations
class Enemy(Character):
    def __init__(self,x, y, width, height,graph,hpImgPath,target=None,collisionRects=None):
        self.target=target
        self.graph = graph
        self.dead = False
        self.attackTimer = 100
        self.imunityFrames = 0
        self.attackRange = pygame.Rect(x,y,width+40,height)
        self.attacking = False
        self.hpBar= self.getHpBar(hpImgPath)
        super().__init__(x, y, width, height,collisionRects)
        self.ai = Ai(self.rect, target,graph)
    
    def getHpBar(self,path):
        hpBar = {} 
        img = pygame.image.load(path)
        img.set_colorkey((0,0,0))
        hpBar['img'] = img
        hpBar['height'] = img.get_height()
        hpBar['hp'] = 100
        return hpBar
    
    @property
    def hpBarWidth(self):
        return self.hpBar['img'].get_width() * (self.hpBar['hp'] / 100)
    
    def drawHpBar(self,surf,scroll):
        pygame.draw.rect(surf,(172,50,50),(self.x-scroll[0],self.y-scroll[1]-10,self.hpBarWidth,self.hpBar['height']))
        surf.blit(self.hpBar['img'],(self.x - scroll[0],self.y - scroll[1] - 10))
    
    def takeDamage(self,damage):
        if self.imunityFrames == 0:
            self.imunityFrames = 10
            self.hpBar['hp'] -= damage
            if self.hpBar['hp'] <= 0:
                self.kill()
        else:
            self.imunityFrames -= 1
    
    def kill(self):
        self.dead = True
    
    def getAnimations(self):
        animations = Animations('assets/enemyAnimations')
        animations.getAnimation('run',[4,4,4,4,4,4,4])
        animations.getAnimation('idle',[6,6,6,6,6,6,6,6])
        animations.getAnimation('attack',[4,4,4,4,4,4,4,4,4,10,4,4,4,4,4,4])
        return animations
    
    def changeAnimationState(self,movement):
        self.attackTimer -= 1 
        if self.attackTimer < 0 and self.x - self.target.x < 50 and self.x - self.target.x > -50 and self.y - self.target.y < 50 and self.y - self.target.y > -50:
            self.attacking = True
            
        if self.attacking == True:
            self.animations.changeState('attack')
            if ((self.animations.getCurrentImg() == 'attack1') or (self.animations.getCurrentImg() == 'attack2') or 
                (self.animations.getCurrentImg() == 'attack3') or (self.animations.getCurrentImg() == 'attack4') or 
                (self.animations.getCurrentImg() == 'attack5')):
                    self.flip = False
                    if self.target.x < self.x:
                        self.flip = True
            if self.animations.getCurrentImg() == 'attack10' or self.animations.getCurrentImg() == 'attack11':
                self.checkForHits()
            elif self.animations.getCurrentImg() == 'attack15':
                self.attackTimer = 100
                self.attacking = False
        else:
            if movement[0] == 0:self.animations.changeState('idle')
            if movement[0] > 0:self.animations.changeState('run')
            if movement[0] < 0:self.animations.changeState('run')

    def setDirectionToMove(self):
        ChangeInleft, ChangeInright, jump = self.ai.getDirection(self.airTimer)
        if ChangeInleft is not None:self.left = ChangeInleft
        if ChangeInright is not None:self.right = ChangeInright
        if jump:self.playerJump()        
    def checkForHits(self):
        if self.attackRange.colliderect(self.target.rect):
            self.target.takeDamage(10)
    def draw(self,surface,scroll,img):
        #pygame.draw.rect(surface,(255,0,0),self.rect)
        a = 0
        if self.flip:
            a = 48
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.x-a-9-scroll[0],self.y-9-scroll[1]))

    def update(self,gameSurface, scroll):  
        self.setDirectionToMove()
        #-------------------------------------------------------------#
        self.x = self.rect.x 
        self.y = self.rect.y
        self.attackRange.x = self.rect.x
        self.attackRange.y = self.rect.y
        if self.flip: self.attackRange.x -= 48
        else: self.attackRange.x += 8
        #-------------------------------------------------------------#
        if not self.attacking: movement = self.move(self.collisionRects)#call the move function
        else:
            movement = [0,0]
            
        self.changeAnimationState(movement)
        self.drawHpBar(gameSurface,scroll)
        self.draw(gameSurface,scroll,self.animations.getImg())#draw the enemy
        
        
           