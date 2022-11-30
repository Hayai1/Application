
import pygame
from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.input import Input

class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        self.world = World(50)
        self.player = Player(self.world.rooms[0],'assets/spriteSheets/oldRoomSpriteSheet.png','assets/spriteSheets/oldRoomSpriteSheet.png')
        self.camera = Camera(self.player)
        self.input = Input(self.player)
    def runGame(self):
        # -------- Main Program Loop -----------
        while True:
            self.input.update()
            self.camera.update()
            self.world.update(self.window.surface,self.camera)
            self.player.update(self.window.surface,self.camera,self.world)
            self.window.update()
    

