#import modules not created by me
#----------------------------------
import pygame
#----------------------------------
#import modules created by me
#----------------------------------
from scripts.world import World
from scripts.player import Player
from scripts.window import Window
from scripts.camera import Camera
from scripts.enemyManager import EnemyManager
from scripts.menuManager import MainMenu
from scripts.dbHandler import DBHandler
from scripts.inGameMenu import InGameMenu,DeathMenu
#----------------------------------

class Game:#game class
    def __init__(self):#constructor function for the game class takes no arguments
        pygame.init()#initialize pygame
        self.window = Window((640,360),"Nea Project",60)#create a new window to display the game on
        self.dbHandler = DBHandler()#create a new dbHandler to handle the database
        self.menu = MainMenu(self.window,self.dbHandler)#create a new menu to display the main menu before starting the game
        self.playerId,self.worldId = self.runMenu()
        #<----------------------World--------------------------->
        self.world = self.createWorld()
        #<----------------------Player-------------------------->
        self.player = self.createPlayer()
        #<----------------------EnemyManager-------------------------->
        self.enemyManager = self.createEnemyManager()
        #<----------------------Camera-------------------------->
        self.camera = self.createCamera()
        

    def createPlayer(self):
        name,hp = self.dbHandler.getPlayerData(self.playerId)#get the player's name and hp from the database
        x,y = self.dbHandler.getPlayerPositionData(self.playerId,self.worldId,self.world.getDefaultPos())#get the player's position from the database
        player = Player(name,x,y,hp, 16, 16,self.world.collisionRects,'assets/hpBar/hpBar.png')#create a new player
        return player#return the player
    def createWorld(self):
        worldName,WorldSeed = self.dbHandler.getWorldData(self.worldId)#get the world's name and seed from the database
        return World(worldName,WorldSeed)#create a new world
    def createEnemyManager(self):
        enemyManager = EnemyManager(20,self.player,self.worldId,self.dbHandler,self.world.rooms,self.world.collisionRects,self.world.graph) #create a new enemyManager with 20 enemies in the world
        return enemyManager#return the enemyManager
    def createCamera(self):
        camera = Camera(self.player)#create a new camera with the player as the target to focus on
        return camera#return the camera
    
    
    @property
    def scroll(self):
        return self.camera.scroll#return the camera's scroll
    @property
    def gameSurface(self):
        return self.window.GameSurface#return the window's game surface
    
    
    def inGameMenu(self):#create the in game menu
        inGameMenu = InGameMenu(self.window,self.playerId,(self.player.x,self.player.y),self.player.hpBar['hp'],self.worldId,self.dbHandler)#create the in game menu
        resume = False#set resume to false
        self.player.input.runInGameMenu = False#set the player's input to not run the in game menu
        while not resume:#while resume is false
            resume = inGameMenu.update()#update the in game menu
            self.window.update()#update the window

    def dead(self):
        self.player.x,self.player.y=self.world.getDefaultPos()#set the player's position to the default position
        deathScreen = DeathMenu(self.window,self.playerId,(self.player.x,self.player.y),self.worldId,self.dbHandler)#create the death menu
        respawn = False#set respawn to false
        self.player.dead = False#set the player's dead variable to false
        while not respawn:#while the user hasn't clicked respawn
            respawn = deathScreen.update()#update the death menu
            self.window.update() #update the window

            
    def updateGame(self):
        self.camera.update()
        self.world.update(self.gameSurface,self.scroll)
        self.enemyManager.update(self.gameSurface,self.scroll)
        self.player.update(self.gameSurface,self.scroll,self.enemyManager.enemies)
        self.window.update()
        if self.player.dead:self.dead()
        if self.player.isInIngameMenu:self.inGameMenu()
        
    def updateMenu(self):
        self.window.update()
        return self.menu.update()
    

    def runGame(self):
        while True:
            self.updateGame()
    
    def runMenu(self):
        while True:
            startGame = self.updateMenu()
            if startGame:break
        return self.menu.playerId, self.menu.worldId
         
    

    

