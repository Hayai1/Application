
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemyManager import EnemyManager
from scripts.menuManager import MenuManager
from scripts.dbHandler import DBHandler
from scripts.background import BackGround

class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((640,360),"Nea Project",60)
        self.dbHandler = DBHandler()
        
        self.menu = MenuManager(self.window,self.dbHandler)
        playerId,worldId = self.runMenu()
        #self.runSqlCommands()
        
        self.camera = Camera()
        worldName,WorldSeed = self.dbHandler.getWorldData(worldId)
        self.world = World(self.window.GameSurface,self.camera,worldName,WorldSeed)
        self.background = BackGround('assets/bg/bg.png')
        self.player = self.getPlayer(playerId,worldId)
        self.camera.set_target(self.player)
        self.enemyManger = EnemyManager(20,self.world.rooms,self.player,self.window.GameSurface,self.camera,self.world.collisionRects,self.world.graph) 

        
        
        

    def getPlayer(self,playerId,worldId):
        name,pos = self.dbHandler.getPlayerData(playerId,worldId)
        if pos == []:pos = self.world.getDefaultPos()
        player = Player(name,pos[0],pos[1], 16, 16,self.window.GameSurface,self.camera,[0,0],hpBarImg='assets/hpBar/hpBar.png')
        player.setRectsToCollideWith(self.world.collisionRects)
        return player

    def runSqlCommands(self):
        while True:
            sqlc = input("sql command:")
            if sqlc == "exit":
                SystemExit
            print(self.dbHandler.db.manualSQLCommand(sqlc))
    
    def update(self):
        self.background.update(self.window.GameSurface,self.camera.scroll)
        self.camera.update()
        self.world.update()
        self.enemyManger.update()
        self.player.update(self.enemyManger.enemies)
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
         
    

    

