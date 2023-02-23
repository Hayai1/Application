import scripts.menuManager as menuManager
import sys


class InGameMenu(menuManager.Menu):
    def __init__(self,window,playerid,playerLoc,worldid,dbHandler):
        self.playerId = playerid
        self.worldId = worldid
        self.playerLoc = playerLoc
        self.dbHandler = dbHandler

        super().__init__(window, dbHandler, self.pauseMenu)

    def resume(self):
        return True
    def save(self):
        self.dbHandler.savePlayerData(self.playerId,self.worldId,self.playerLoc)
        return True
    def exit(self):
        sys.exit()

    def pauseMenu(self):
        text1 = menuManager.Text(self.window.GameSurface,'PAUSED',(0,0),isButton=False)
        text2 = menuManager.Text(self.window.GameSurface,'RESUME',(0,50),isButton=True,menuAddress=self.resume)
        text3 = menuManager.Text(self.window.GameSurface,'SAVE',(0,100),isButton=True,menuAddress=self.save)
        text4 = menuManager.Text(self.window.GameSurface,'EXIT',(0,150),isButton=True,menuAddress=self.exit)
        return menuManager.MenuScreen(self.window,self.cursor,text1,text2,text3,text4)


class DeathMenu(menuManager.Menu):
    def __init__(self,window,playerId,spawnLoc,worldId,dbHandler):
        super().__init__(window, dbHandler, self.deathMenu)
        self.dbHandler.savePlayerData(playerId,worldId,spawnLoc)
        

    def respawn(self):
        return True

    def exit(self):
        sys.exit()

    def deathMenu(self):
        text1 = menuManager.Text(self.window.GameSurface,'YOU DIED',(0,0),isButton=False)
        text2 = menuManager.Text(self.window.GameSurface,'RESPAWN',(0,50),isButton=True,menuAddress=self.respawn)
        text3 = menuManager.Text(self.window.GameSurface,'EXIT',(0,100),isButton=True,menuAddress=self.exit)
        return menuManager.MenuScreen(self.window,self.cursor,text1,text2,text3)