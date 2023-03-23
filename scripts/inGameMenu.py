import scripts.menuManager as menuManager
import sys


class InGameMenu(menuManager.Menu):# this is the menu that will be displayed when the player presses escape
    def __init__(self,window,playerid,playerLoc,playerHp,worldid,dbHandler):#create the menu
        self.playerId = playerid# the id of the player
        self.worldId = worldid# the id of the world
        self.playerHp = playerHp# the hp of the player
        self.playerLoc = playerLoc# the location of the player
        self.dbHandler = dbHandler# the database handler


        super().__init__(window, dbHandler, self.pauseMenu)# create the menu with the pause menu as the first menu

    def resume(self):# resume the game
        return True# return true to tell the game to resume
    def save(self):# save the game
        self.dbHandler.updatePlayerPosInSpecificWorld(self.playerId,self.worldId,self.playerLoc)# update the player's position in the database
        self.dbHandler.updatePlayerHp(self.playerId,self.playerHp)# update the player's hp in the database
        return True# return true to tell the game to resume
    def exit(self):# exit the game
        sys.exit()# exit the game

    def pauseMenu(self):
        text1 = menuManager.Text(self.window.GameSurface,'PAUSED',(0,0),isButton=False)
        text2 = menuManager.Text(self.window.GameSurface,'RESUME',(0,50),isButton=True,menuAddress=self.resume)
        text3 = menuManager.Text(self.window.GameSurface,'SAVE',(0,100),isButton=True,menuAddress=self.save)
        text4 = menuManager.Text(self.window.GameSurface,'EXIT',(0,150),isButton=True,menuAddress=self.exit)
        return menuManager.MenuScreen(self.window,self.cursor,text1,text2,text3,text4)


class DeathMenu(menuManager.Menu):
    def __init__(self,window,playerId,spawnLoc,worldId,dbHandler):
        super().__init__(window, dbHandler, self.deathMenu)
        self.dbHandler.updatePlayerPosInSpecificWorld(playerId,worldId,spawnLoc)
        

    def respawn(self):
        return True

    def exit(self):
        sys.exit()

    def deathMenu(self):
        text1 = menuManager.Text(self.window.GameSurface,'YOU DIED',(0,0),isButton=False)
        text2 = menuManager.Text(self.window.GameSurface,'RESPAWN',(0,50),isButton=True,menuAddress=self.respawn)
        text3 = menuManager.Text(self.window.GameSurface,'EXIT',(0,100),isButton=True,menuAddress=self.exit)
        return menuManager.MenuScreen(self.window,self.cursor,text1,text2,text3)