import pygame
from character import Character
#Player attributes, plus some other globals that shouldn't be here...


class Player(Character):
    name = "Player"
    def update(self,surface,scroll):
        self.move()
        self.drawPlayer(surface,scroll)