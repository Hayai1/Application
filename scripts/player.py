import pygame
from scripts.character import Character
from scripts.animations import Animations
class Player(Character):
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

    



        