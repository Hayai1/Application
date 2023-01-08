
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemy import Enemy
from scripts.menuManager import MenuManager
class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        self.menu = MenuManager(self.window)
        self.runMenu()
        self.camera = Camera()
        self.world = World(self.window.surface,self.camera,50)
        self.player = Player(self.world.graphRects[0].x+8*16,self.world.graphRects[0].y+16, 16, 16,self.window.surface,self.camera,[0,0])
        self.enemies = []
        self.enemy1 = Enemy(self.world.graphRects[0].x+8*16,self.world.graphRects[0].y+16, 16, 16,self.world.graph,'assets/playerAnimations/idle/idle0.png',[0,0],target=self.player,surf=self.window.surface,camera=self.camera,collisionRects=self.world.collisionRects)
        self.enemies.append(self.enemy1)
        self.player.setRectsToCollideWith(self.world.collisionRects)
        self.camera.set_target(self.player)
    
    def update(self):
        self.camera.update()
        self.world.update()
        for enemy in self.enemies:
            enemy.update()
        self.player.update()
        self.window.update()
        
    def runGame(self):
        while True:
            self.update()
    def runMenu(self):
        while True:
            startGame = self.menu.update()
            self.window.update()
            if startGame:
                break
        
    

    

