import pygame
from scripts.character import Character

class Player(Character):
    
    def update(self,world1,surface,camera):
        self.move(world1.rects)
        self.drawPlayer(surface,camera.scroll)
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

    



        