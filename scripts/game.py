
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
        #<----------------------World--------------------------->
        self.world = self.getWorld(worldId)
        #<----------------------Player-------------------------->
        self.player = self.getPlayer(playerId,worldId)
        #<----------------------EnemyManager-------------------------->
        self.enemyManager = EnemyManager(20,self.world.rooms,self.player,self.world.collisionRects,self.world.graph) 
        #<----------------------Background-------------------------->
        self.background = BackGround('assets/bg/bg.png')
        #<----------------------Camera-------------------------->
        self.camera = Camera(self.player)
        

    def getPlayer(self,playerId,worldId):
        name,x,y = self.dbHandler.getPlayerData(playerId,worldId)
        if x ==0 and y ==0:
            x,y = self.world.getDefaultPos()
        player = Player(name,x,y, 16, 16,self.world.collisionRects,'assets/hpBar/hpBar.png')
        return player
    def getWorld(self,worldId):
        worldName,WorldSeed = self.dbHandler.getWorldData(worldId)
        return World(worldName,WorldSeed)
    
    def runSqlCommands(self):
        while True:
            sqlc = input("sql command:")
            if sqlc == "exit":
                SystemExit
            print(self.dbHandler.db.manualSQLCommand(sqlc))
    
    @property
    def scroll(self):
        return self.camera.scroll
    @property
    def gameSurface(self):
        return self.window.GameSurface
    
    def update(self):
        self.camera.update()
        self.background.update(self.gameSurface,self.scroll)
        self.world.update(self.gameSurface,self.scroll)
        self.enemyManager.update(self.gameSurface,self.scroll)
        self.player.update(self.gameSurface,self.scroll,self.enemyManager.enemies)
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
         
    

    

