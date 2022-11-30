import pygame
from scripts.character import Character
from scripts.animations import Animations
from scripts.sword import Sword
class Player(Character):
    def __init__(self, room, swordThumbnailPath, swordUseImgPath):
        self.weapons = {'sword' : Sword(swordThumbnailPath,swordUseImgPath)}
        self.takeInputs = True
        self.attack = False
        super().__init__(room)
    def getAnimations(self):
        animations = Animations('assets/playerAnimations')
        animations.getAnimation('run',[4,4,4,4,4])
        animations.getAnimation('idle',[1])
        animations.getAnimation('attack',[6,6,6,6,4,4,4])
        return animations

    def update(self,surface,camera,world):
        self.move(world.rects)
        if not self.attack:
            if self.velocity[0] == 0:
                self.animations.changeState('idle')
            if self.velocity[0] > 0:
                self.flip = False
                self.animations.changeState('run')
            if self.velocity[0] < 0:
                self.flip = True
                self.animations.changeState('run')

        if self.attack:
            self.animations.changeState('attack')
            currentImg = self.animations.getCurrentImg()
            if currentImg == 'attack4':
                self.weapons['sword'].swing()
            elif currentImg == 'attack6':
                self.attack = False
            

        self.weapons['sword'].update(surface,camera.scroll,self.rect.x,self.rect.y,self.flip)
        if self.weapons['sword'].arcDone:
           self.takeInputs = True
        else:
            self.takeInputs = False
        self.velocity = [0,0]
        self.draw(surface,camera.scroll)
    



        