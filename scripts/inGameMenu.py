import scripts.menuManager as menuManager
import sys


class InGameMenu:
    def __init__(self,window,playerid,playerLoc,worldid,dbHandler):
        self.window = window
        self.playerId = playerid
        self.worldId = worldid
        self.playerLoc = playerLoc
        self.dbHandler = dbHandler
        self.cursor = menuManager.Cursor(window)
        self.input = menuManager.MenuInput()
        self.click = False
        self.currentMenu = self.pauseMenu()
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
        return menuManager.Menu(self.window,self.cursor,text1,text2,text3,text4)

    def update(self):
        self.input.update()
        inputs = self.input.key
        menuAddress = self.currentMenu.update(inputs)
        if menuAddress != None:
            return menuAddress()
        self.cursor.update()
        return False