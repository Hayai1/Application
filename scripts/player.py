import pygame
from scripts.character import Character
from scripts.animations import Animations
from scripts.sword import Sword
from scripts.playerInput import PlayerInput
class Player(Character):
    def __init__(self,name,x, y, width, height,surface,camera,velocity,acceleration=[0,0],hpBarImg=None,swordThumbnailPath=None, swordUseImgPath=None):
        self.name = name
        self.surface = surface
        self.camera = camera
        self.weapons = {'sword' : Sword(x,y,swordThumbnailPath,swordUseImgPath)}
        self.takeInputs = True
        self.attack = False
        self.dash = False
        self.input = PlayerInput(self)
        self.hpBarImg = pygame.image.load(hpBarImg)
        self.hpBarImg.set_colorkey((0,0,0))
        self.dashAcceleration = 0.5
        self.slide = False
        self.slideVel = None
        self.slideAcc = None

        super().__init__(x, y, width, height,velocity,acceleration)

    def getAnimations(self):
        animations = Animations('assets/playerAnimations')
        animations.getAnimation('run',[4,4,4,4,4])
        animations.getAnimation('idle',[1])
        animations.getAnimation('attack',[4,4,4,4,4,4])
        animations.getAnimation('dash',[4,5,5,5,5,5])
        return animations
    def drawPlayerHpBar(self):
        self.surface.blit(self.hpBarImg,(4,4))
        pygame.draw.rect(self.surface,(255,0,0),(5,5,self.hp,6))
    def triggerAttack(self):
        self.animations.changeState('attack')
        currentImg = self.animations.getCurrentImg()
        if currentImg == 'attack3':
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip)
            self.startSlide()
        elif currentImg == 'attack5':self.attack = False
    def triggerDash(self):
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
    def startSlide(self):
        self.slideVel = 3
        self.slideAcc = -1
        self.slide = True
    def update(self):
        self.x = self.rect.x 
        self.y = self.rect.y
        self.input.update()
        if not self.attack:
            movement = self.move(self.rectsToCollideWith)
        if self.dash: self.triggerDash()
        elif self.attack: 
            self.triggerAttack()
        else: self.changeAnimationState(movement)

        if self.slide:
            self.slideVel += self.slideAcc
            if self.flip: self.x -=self.slideVel
            else: self.x += self.slideVel
            if self.slideVel <= 0:
                self.slide = False
                self.slideVel = None
                self.slideAcc = None
        self.weapons['sword'].update(self.x,self.y,self.surface,self.camera.scroll)
        self.draw(self.surface,self.camera.scroll,self.animations.getImg())
    



        