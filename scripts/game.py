
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
        self.surface = self.window.createNewSurface((300,200))
        self.world = World(50)
        self.player = Player(0,0)
        self.camera = Camera(self.player)
        self.input = Input()
    def runGame(self):
        # -------- Main Program Loop -----------
        while True:
            self.window.screen.fill((0,0,0))
            self.input.update(self.player)
            self.camera.update()
            self.surface.fill((0,0,0))
            self.world.update(self.surface, self.camera)
            self.player.update(self.world,self.surface,self.camera)
            self.window.update(self.surface)
    

