
import pygame, time
from scripts.ai import Ai
from scripts.character import Character
from scripts.animations import Animations
from scripts.vfx import Vfx
class Enemy(Character):#the enemy class (inherits from the character class)
    def __init__(self,x, y, width, height,graph,hpImgPath,target=None,collisionRects=None, damageMult = 1,hpMult = 1):#create the enemy
        super().__init__(x, y, width, height,collisionRects)#call the super class
        self.target=target#the target to focus on
        self.graph = graph#the graph
        self.dead = False#is the enemy dead
        self.damage = 10 * damageMult#the damage of the enemy
        self.attackTimer = 100#the attack timer
        self.imunityFrames = 0#the imunity frames
        self.attackRange = pygame.Rect(x,y,width+40,height)#the attack range
        self.attacking = False#is the enemy attacking
        self.animations = self.getAnimations('assets/enemyAnimations',run=[4,4,4,4,4,4,4],idle=[6,6,6,6,6,6,6,6],attack=[4,4,4,4,4,4,4,4,4,10,4,4,4,4,4,4])#get the animations
        self.maxHp = self.maxHp*hpMult#set the max hp
        self.hpBar= self.getHpBar(self.maxHp,hpImgPath)#get the hp bar
        self.ai = Ai(self.rect, target,graph)#create the ai
    
    
    
    def drawHpBar(self,surf,scroll):#draw the hp bar
        pygame.draw.rect(surf,(172,50,50),(self.x-scroll[0],self.y-scroll[1]-10,self.hpBarWidth,self.hpBar['height']))#draw the hp bar
        surf.blit(self.hpBar['img'],(self.x - scroll[0],self.y - scroll[1] - 10))#draw the hp bar image
    

    
    def kill(self):#kill the enemy
        self.dead = True#set dead to true
    
    def inAggroRange(self,Pos,targetPos):#is the enemy in aggro range
        if Pos[0] - targetPos[0] < 50 and Pos[0] - targetPos[0] > -50 and Pos[1] - targetPos[1] < 50 and Pos[1] - targetPos[1] > -50:return True#return true if the enemy is in aggro range (50x50px around the enemy)
        return False#return false
    def changeAnimationState(self,movement):#change the animation state
        self.attackTimer -= 1 #decrease the attack timer
        if self.attackTimer < 0 and self.inAggroRange((self.x,self.y),(self.target.x,self.target.y)):#if the attack timer is less than 0 and the enemy is in aggro range
            self.attacking = True#set attacking to true
            
        if self.attacking == True:#if the enemy is attacking
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
        if jump:self.jump()        
    def checkForHits(self):
        self.attackRange.x = self.rect.x
        self.attackRange.y = self.rect.y
        if self.flip: self.attackRange.x -= 48
        else: self.attackRange.x += 8
        if self.attackRange.colliderect(self.target.rect):
            self.target.takeDamage(self.damage)

    def draw(self,surface,scroll,img):
        flipDecrease = 0
        if self.flip:
            flipDecrease = 48
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.x-flipDecrease-9-scroll[0],self.y-9-scroll[1]))

    def update(self,gameSurface, scroll):
        self.updateCharacter()
        self.setDirectionToMove()
        movement = [0,0]
        if not self.attacking: movement = self.move(self.collisionRects)#call the move function
        self.changeAnimationState(movement)
        self.drawHpBar(gameSurface,scroll)
        self.draw(gameSurface,scroll,self.animations.getImg())#draw the enemy
        
        
           