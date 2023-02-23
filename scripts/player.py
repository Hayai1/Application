import pygame,sys
from scripts.character import Character
from scripts.animations import Animations
from scripts.sword import Sword
from scripts.playerInput import PlayerInput
class Player(Character):
    def __init__(self,name,x, y,hp, width, height,collisionRects,hpBarImg=None,swordThumbnailPath=None, swordUseImgPath=None):
        self.name = name
        self.weapons = {'sword' : Sword(x,y,swordThumbnailPath,swordUseImgPath)}
        self.takeInputs = True
        self.attacking = False
        self.dash = False
        self.input = PlayerInput(self)
        self.dashAcceleration = 0.5
        self.slide = False
        self.slideVel = None
        self.slideAcc = None
        self.imunityFrames = 0
        self.dead = False
        self.attackCombo = 'firstAttack'
        self.hpBar = self.getHpBar(hp,hpBarImg)
        super().__init__(x, y, width, height,collisionRects)

    def getAnimations(self):
        animations = Animations('assets/playerAnimations')
        animations.getAnimation('run',[4,4,4,4,4])
        animations.getAnimation('idle',[1])
        animations.getAnimation('firstAttack',[4,4,4,4,4,4])
        animations.getAnimation('secondAttack',[5,5,4,4])
        animations.getAnimation('thirdAttack',[5,10,4])
        animations.getAnimation('dash',[4,5,5,5,5,5])
        return animations
    def getHpBar(self,hp,path):
        hpBar = {} 
        img = pygame.image.load(path)
        img.set_colorkey((0,0,0))
        hpBar['img'] = img
        hpBar['height'] = img.get_height()-10
        hpBar['hp'] = hp
        return hpBar
    def resetHpBar(self):
        self.hpBar['hp'] = 100
    @property
    def hpBarWidth(self):
        return (self.hpBar['img'].get_width()-10) * (self.hpBar['hp'] / 100)
    def drawPlayerHpBar(self,gameSurface):
        pygame.draw.rect(gameSurface,(172,50,50),(9,9+170,self.hpBarWidth,self.hpBar['height']))
        gameSurface.blit(self.hpBar['img'],(4,4+170))
    def attack(self):
        if self.attackCombo =='firstAttack':
            self.triggerAttack1()
        elif self.attackCombo == 'secondAttack':
            self.triggerAttack2()
        elif self.attackCombo == 'thirdAttack':
            self.triggerAttack3()
        
    def triggerAttack1(self):
        self.animations.changeState('firstAttack')
        currentImg = self.animations.getCurrentImg()
        if currentImg == 'firstAttack2':
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip,'down')
            self.startSlide()
        elif currentImg == 'firstAttack5':
            self.attacking = False
            self.attackCombo = 'secondAttack'

    def triggerAttack2(self):
        self.animations.changeState('secondAttack')
        currentImg = self.animations.getCurrentImg()
        if currentImg == 'secondAttack2':
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip,'up')
            self.startSlide()
        elif currentImg == 'secondAttack3':
            self.attacking = False
            self.attackCombo = 'thirdAttack'
    def triggerAttack3(self):
        self.animations.changeState('thirdAttack')
        currentImg = self.animations.getCurrentImg()
        if currentImg == 'thirdAttack0':
            self.startSlide()
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip,'down')
            
        elif currentImg == 'thirdAttack2':
            self.attacking = False
            self.attackCombo = 'firstAttack'
    def triggerDash(self):
        self.attacking = False
        if self.flip: 
            self.velocity[0] = -(6 / self.dashAcceleration)
            self.dashAcceleration += 0.5
        else: 
            self.velocity[0] = (6 / self.dashAcceleration)
            self.dashAcceleration += 0.5
        self.animations.changeState('dash')
        currentImg = self.animations.getCurrentImg()
        if currentImg == 'dash5':
            self.dash = False
            self.dashAcceleration = 0.5
    def changeAnimationState(self,movement):
        if movement[0] == 0:self.animations.changeState('idle')
        if movement[0] > 0:self.animations.changeState('run')
        if movement[0] < 0:self.animations.changeState('run')
    def takeDamage(self,damage):
        if self.imunityFrames <= 0:
            self.imunityFrames = 100
            self.hpBar['hp'] -= damage
            if self.hpBar['hp'] <= 0:
                self.kill()

    def kill(self):
        self.dead = True
    def startSlide(self):
        self.slideVel = 3
        self.slideAcc = -1
        self.slide = True
    def update(self,gameSurface,scroll, enemies):
        self.imunityFrames -= 1
        self.x = self.rect.x 
        self.y = self.rect.y
        self.input.update()
        if not self.attacking:
            movement = self.move(self.collisionRects)
        if self.dash: self.triggerDash()
        elif self.attacking: 
            self.attack()
        else: self.changeAnimationState(movement)

        if self.slide:
            self.slideVel += self.slideAcc
            if self.flip: self.x -=self.slideVel
            else: self.x += self.slideVel
            if self.slideVel <= 0:
                self.slide = False
                self.slideVel = None
                self.slideAcc = None
        add = 0
        if self.animations.getCurrentImg()[:-1] == 'thirdAttack':
            if self.flip: add = -13
            else: add = 13
        self.weapons['sword'].update(self.x+add,self.y,gameSurface,scroll,enemies)
        
        self.draw(gameSurface,scroll,self.animations.getImg())
        self.drawPlayerHpBar(gameSurface)
    



        