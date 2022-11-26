import pygame
from scripts.character import Character
from scripts.animations import Animations
from scripts.sword import Sword
class Player(Character):
    def __init__(self, room, swordThumbnailPath, swordUseImgPath):
        self.weapons = {'sword' : Sword(swordThumbnailPath,swordUseImgPath)}
        super().__init__(room)
    def getAnimations(self):
        animations = Animations('assets/playerAnimations')
        animations.getAnimation('run',[4,4,4,4,4])
        animations.getAnimation('idle',[1])
        return animations

    def update(self,world,surface,camera):
        self.move(world.rects)
        if self.velocity[0] == 0:
            self.animations.changeState('idle')
        if self.velocity[0] > 0:
            self.flip = False
            self.animations.changeState('run')
        if self.velocity[0] < 0:
            self.flip = True
            self.animations.changeState('run')
        self.velocity = [0,0]
        self.draw(surface,camera.scroll)
        for weapon in self.weapons:
            self.weapons[weapon].update(surface,camera)
            surface.blit(self.weapons[weapon].sword,(self.rect.x-50-camera.scroll[0], self.rect.y-50-camera.scroll[1]))
    def inAggroRange(self,character):
        if abs(self.rect.x - character.rect.x) < 150 and abs(self.rect.y - character.rect.y) < 150:
            return True
        else:
            return False
    def inAttackRange(self,character):
        if abs(self.rect.x - character.rect.x) < 100 and abs(self.rect.y - character.rect.y) < 100:
            return True
        else:
            return False

    



        