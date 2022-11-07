import pygame
from character import Character
#Player attributes, plus some other globals that shouldn't be here...
PLAYER_W = 27
PLAYER_COL = [0,0,200]
JUMP_FORCE = -9
#JUMP_FORCE = -13
GRAVITY = 30
MAX_SPEED = 4
FPS = 60
collidable = (1,2,3)

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

    



        