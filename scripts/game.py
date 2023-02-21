
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
        
        
        worldName,WorldSeed = self.dbHandler.getWorldData(worldId)
        self.world = World(worldName,WorldSeed)
        self.background = BackGround('assets/bg/bg.png')
        #<----------------------Player-------------------------->
        #self.player = self.getPlayer(playerId,worldId)
        name,pos = self.dbHandler.getPlayerData(playerId,worldId)
        if pos == []:pos = self.world.getDefaultPos()
        self.player = Player(name,pos[0],pos[1], 16, 16,hpBarImg='assets/hpBar/hpBar.png')
        self.player.setRectsToCollideWith(self.world.collisionRects)
        #<------------------------------------------------------->
        self.camera = Camera(self.player)
        self.enemyManager = EnemyManager(20,self.world.rooms,self.player,self.world.collisionRects,self.world.graph) 

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
         
    

    

