
import pygame
from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        self.camera = Camera()
        self.player = Player(self.window.surface,self.camera)
        self.world = World(self.window.surface,self.camera,50)

        self.player.setPlayerStartLoc(self.world.rooms[0])
        self.player.setRectsToCollideWith(self.world.rects)
        self.camera.set_target(self.player)

    def update(self):
        self.camera.update()
        self.world.update()
        self.player.update()
        self.window.update()
        
    def runGame(self):
        while True:
            self.update()
    

