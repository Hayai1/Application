
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemyManager import EnemyManager
from scripts.menuManager import MenuManager
from scripts.dbHandler import DBHandler


class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((700,500),"Nea Project",60)
        
        
        self.dbHandler = DBHandler()
        
        self.menu = MenuManager(self.window,self.dbHandler)
        playerId,worldId = self.runMenu()

    
        self.camera = Camera()
        
        self.world = World(self.window.GameSurface,self.camera,30)
        
        name,x,y = self.dbHandler.getPlayerData(playerId,worldId,[self.world.rooms[0].graphRects[0].x+8*16,self.world.rooms[0].graphRects[0].y+16])
        self.player = Player(name,x,y, 16, 16,self.window.GameSurface,self.camera,[0,0],hpBarImg='assets/hpBar/hpBar2.png')
        self.enemyManger = EnemyManager(10,self.world.rooms,self.player,self.window.GameSurface,self.camera,self.world.collisionRects,self.world.graph) 

        
        self.player.setRectsToCollideWith(self.world.collisionRects)
        self.camera.set_target(self.player)
        
    
    def update(self):
        self.camera.update()
        self.world.update()
        self.enemyManger.update()
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
         
    

    

