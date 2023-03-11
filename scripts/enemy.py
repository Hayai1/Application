
import pygame, time
from scripts.ai import Ai
from scripts.character import Character
from scripts.animations import Animations
from scripts.vfx import Vfx
class Enemy(Character):
    def __init__(self,x, y, width, height,graph,hpImgPath,target=None,collisionRects=None, damageMult = 1,hpMult = 1):
        self.target=target
        self.graph = graph
        self.dead = False
        self.damage = 10 * damageMult
        self.attackTimer = 100
        self.imunityFrames = 0
        self.attackRange = pygame.Rect(x,y,width+40,height)
        self.attacking = False
        super().__init__(x, y, width, height,collisionRects)
        self.animations = self.getAnimations('assets/enemyAnimations',run=[4,4,4,4,4,4,4],idle=[6,6,6,6,6,6,6,6],attack=[4,4,4,4,4,4,4,4,4,10,4,4,4,4,4,4])
        self.maxHp = self.maxHp*hpMult
        self.hpBar= self.getHpBar(self.maxHp,hpImgPath)
        self.ai = Ai(self.rect, target,graph)
    
    
    
    def drawHpBar(self,surf,scroll):
        pygame.draw.rect(surf,(172,50,50),(self.x-scroll[0],self.y-scroll[1]-10,self.hpBarWidth,self.hpBar['height']))
        surf.blit(self.hpBar['img'],(self.x - scroll[0],self.y - scroll[1] - 10))
    

    
    def kill(self):
        self.dead = True
    
    
    def changeAnimationState(self,movement):
        self.attackTimer -= 1 
        if self.attackTimer < 0 and self.x - self.target.x < 50 and self.x - self.target.x > -50 and self.y - self.target.y < 50 and self.y - self.target.y > -50:
            self.attacking = True
            
        if self.attacking == True:
            self.animations.changeState('attack')
            if ((self.animations.getCurrentImg()[:-1] == 'attack') and (self.animations.getCurrentImg()[-1] in (1,2,3))):
                    self.flip = False
                    if self.target.x < self.x:
                        self.flip = True
            if self.animations.getCurrentImg() in ('attack10','attack11'):
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
            self.target.takeDamage(self.damage)
    def draw(self,surface,scroll,img):
        #pygame.draw.rect(surface,(255,0,0),self.rect)
        a = 0
        if self.flip:
            a = 48
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.x-a-9-scroll[0],self.y-9-scroll[1]))

    def update(self,gameSurface, scroll):
        self.setDirectionToMove()#
        self.updateCharacter()
        #-------------------------------------------------------------#
        self.attackRange.x = self.rect.x
        self.attackRange.y = self.rect.y
        if self.flip: self.attackRange.x -= 48
        else: self.attackRange.x += 8
        #-------------------------------------------------------------#
        if not self.attacking: movement = self.move(self.collisionRects)#call the move function
        else:movement = [0,0]
        self.changeAnimationState(movement)
        self.drawHpBar(gameSurface,scroll)
        self.draw(gameSurface,scroll,self.animations.getImg())#draw the enemy
        
        
           