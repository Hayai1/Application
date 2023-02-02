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
        self.input = PlayerInput(self)
        self.hpBarImg = pygame.image.load(hpBarImg)
        self.hpBarImg.set_colorkey((0,0,0))
        super().__init__(x, y, width, height,velocity,acceleration)

    def getAnimations(self):
        animations = Animations('assets/playerAnimations')
        animations.getAnimation('run',[4,4,4,4,4])
        animations.getAnimation('idle',[1])
        animations.getAnimation('attack',[6,6,6,6,4,4,4])
        return animations
    def drawPlayerHpBar(self):
        self.surface.blit(self.hpBarImg,(4,4))
        pygame.draw.rect(self.surface,(255,0,0),(5,5,self.hp,6))

    def update(self):
        self.input.update()
        movement = self.move(self.rectsToCollideWith)
        if not self.attack:
            if movement[0] == 0:
                self.animations.changeState('idle')
            if movement[0] > 0:
                self.flip = False
                self.animations.changeState('run')
            if movement[0] < 0:
                self.flip = True
                self.animations.changeState('run')
        if self.attack:
            self.animations.changeState('attack')
            currentImg = self.animations.getCurrentImg()
            if currentImg == 'attack4':
                self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip)
            elif currentImg == 'attack6':
                self.attack = False
        self.weapons['sword'].update(self.x,self.y,self.surface,self.camera.scroll)
        img = self.animations.getImg()
        self.draw(self.surface,self.camera.scroll,img)
        self.drawPlayerHpBar()
    



        