
import pygame
import time

from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemyManager import EnemyManager
from scripts.menuManager import MainMenu
from scripts.dbHandler import DBHandler
from scripts.background import BackGround
from scripts.inGameMenu import InGameMenu
from scripts.inGameMenu import DeathMenu
class Game:
    def __init__(self):
        pygame.init()
        self.window = Window((640,360),"Nea Project",60)
        self.dbHandler = DBHandler()
        self.menu = MainMenu(self.window,self.dbHandler)
        self.playerId,self.worldId = self.runMenu()
        #self.runSqlCommands()
        #<----------------------World--------------------------->
        self.world = self.getWorld(self.worldId)
        #self.runSqlCommands()
        #<----------------------Player-------------------------->
        self.player = self.getPlayer(self.playerId,self.worldId)
        
        #<----------------------EnemyManager-------------------------->
        self.enemyManager = EnemyManager(20,self.world.rooms,self.worldId ,self.dbHandler,self.player,self.world.collisionRects,self.world.graph) 
        #<----------------------Background-------------------------->
        self.background = BackGround('assets/bg/bg.png')
        #<----------------------Camera-------------------------->
        self.camera = Camera(self.player)
        

    def getPlayer(self,playerId,worldId):
        name,hp,x,y = self.dbHandler.getPlayerData(playerId,worldId,self.world.getDefaultPos())
        player = Player(name,x,y,hp, 16, 16,self.world.collisionRects,'assets/hpBar/hpBar.png')
        return player
    def getWorld(self,worldId):
        worldName,WorldSeed = self.dbHandler.getWorldData(worldId)
        return World(worldName,WorldSeed)
    
    def runSqlCommands(self):
        while True:
            sqlc = input("sql command:")
            if sqlc == "exit":
                return
            print(self.dbHandler.db.manualSQLCommand(sqlc))
    
    @property
    def scroll(self):
        return self.camera.scroll
    @property
    def gameSurface(self):
        return self.window.GameSurface
    def extraUpdates(self):
        if self.player.dead:
            x,y=self.world.getDefaultPos()
            self.player.x = x
            self.player.y = y
            self.player.resetHpBar = 100
            deathScreen = DeathMenu(self.window,self.playerId,(self.player.x,self.player.y),self.worldId,self.dbHandler)
            respawn = False
            self.player.dead = False
            while not respawn:
                respawn = deathScreen.update()
                self.window.update()
        if self.player.input.runInGameMenu:
            inGameMenu = InGameMenu(self.window,self.playerId,(self.player.x,self.player.y),self.player.hpBar['hp'],self.worldId,self.dbHandler)
            resume = False
            self.player.input.runInGameMenu = False
            while not resume:
                resume = inGameMenu.update()
                self.window.update()
        
                
            
    def update(self):
        self.camera.update()
        self.background.update(self.gameSurface,self.scroll)
        self.world.update(self.gameSurface,self.scroll)
        self.enemyManager.update(self.gameSurface,self.scroll)
        self.player.update(self.gameSurface,self.scroll,self.enemyManager.enemies)
        self.window.update()
        self.extraUpdates()
        
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
         
    

    

