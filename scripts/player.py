import pygame
from scripts.character import Character
from scripts.animations import Animations
from scripts.sword import Sword
from scripts.playerInput import PlayerInput
class Player(Character):
    def __init__(self,name,x, y, width, height,surface,camera,velocity,acceleration=[0,0],swordThumbnailPath=None, swordUseImgPath=None):
        self.name = name
        self.surface = surface
        self.camera = camera
        self.weapons = {'sword' : Sword(swordThumbnailPath,swordUseImgPath)}
        self.takeInputs = True
        self.attack = False
        self.input = PlayerInput(self)
        super().__init__(x, y, width, height,velocity,acceleration)
        
    def getAnimations(self):
        animations = Animations('assets/playerAnimations')
        animations.getAnimation('run',[4,4,4,4,4])
        animations.getAnimation('idle',[1])
        animations.getAnimation('attack',[6,6,6,6,4,4,4])
        return animations

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
                self.weapons['sword'].swing()
            elif currentImg == 'attack6':
                self.attack = False
            

        self.weapons['sword'].update(self.surface,self.camera.scroll,self.rect.x,self.rect.y,self.flip)
        if self.weapons['sword'].arcDone:
           self.takeInputs = True
        else:
            self.takeInputs = False
        
        self.draw(self.surface,self.camera.scroll)
    



        