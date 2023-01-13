
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemy import Enemy
from scripts.menuManager import MenuManager
from scripts.dataBaseClasses import DBHandler
class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        
        
        self.dbHandler = DBHandler()
        
        self.menu = MenuManager(self.window,self.dbHandler)
        playerId,worldId = self.runMenu()

    
        self.camera = Camera()
        
        self.world = World(self.window.surface,self.camera,50)
        
        name,x,y = self.dbHandler.getPlayerData(playerId,worldId,[self.world.graphRects[0].x+8*16,self.world.graphRects[0].y+16])
        self.player = Player(name,x,y, 16, 16,self.window.surface,self.camera,[0,0])
        
        self.enemies = []
        self.enemy1 = Enemy(self.world.rooms[0].graphRects[0].x+8*16,self.world.rooms[0].graphRects[0].y+16, 16, 16,self.world.graph,'assets/playerAnimations/idle/idle0.png',[0,0],target=self.player,surf=self.window.surface,camera=self.camera,collisionRects=self.world.collisionRects)
        self.enemies.append(self.enemy1)
        
        
        self.player.setRectsToCollideWith(self.world.collisionRects)
        self.camera.set_target(self.player)
        self.player.input.enemy = self.enemy1
    
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
            runGame = self.menu.update()
            self.window.update()
            if runGame:
                break
        return self.menu.playerId, self.menu.worldId
         
    

    

