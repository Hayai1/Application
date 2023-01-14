import pygame, string,sys, os
from scripts.menuInput import MenuInput
from scripts.dbHandler import *

class MenuManager:
    def __init__(self,window,dbHandler):
        self.window = window
        self.dbHandler = dbHandler
        self.cursor = Cursor()
        self.input = MenuInput()
        self.currentMenu = self.startMenu()
        self.click = False

        self.playerName = None
        self.worldName = None
        self.worldDifficulty = None
        
        self.playerId = None
        self.worldId = None

    def setPlayerName(self,value):
        self.playerName = value
    def setWorldName(self,value):
        self.worldName = value
    #when difficulty is set all data is achieved hence the game will start
    def hard(self):
        self.worldDifficulty = 3
        return self.createWorld()
    def normal(self):
        self.worldDifficulty = 2
        return self.createWorld()
    def easy(self):
        self.worldDifficulty = 1
        return self.createWorld()
    def createWorld(self):
        self.worldId = self.dbHandler.createWorldRecord(self.worldName,self.worldDifficulty)
        return self.exitMenu()
    def exitMenu(self):
        return 'exit'
    def createCharacter(self):
        #create the character
        self.playerId = self.dbHandler.createCharacterRecord(self.playerName)
        return self.worldMenu()
    
    

        

    def startMenu(self):
        text1 = Text(self.window,'GAME NAME',(0,0),isButton=False)
        text2 = Text(self.window,'START',(0,50),isButton=True,menuAddress=self.characterMenu)
        text3 = Text(self.window,'EXIT',(0,100),isButton=True,menuAddress=sys.exit)
        return Menu(self.window,self.cursor,text1,text2,text3)
        
    def characterMenu(self):
        text1 = Text(self.window,'CHARACTERS',(0,0),isButton=False)
        text2 = Text(self.window,'CREATE NEW CHARACTER',(0,50),isButton=True,menuAddress=self.characterCreationMenuEnterName)
        text3 = Text(self.window,'CHARACTER LIST',(0,100),isButton=True,menuAddress=self.worldMenu)
        text4 = Text(self.window,'BACK',(0,150),isButton=True,menuAddress=self.startMenu)
        return Menu(self.window,self.cursor,text1,text2,text3,text4)
    def characterCreationMenuEnterName(self):
        text1 = Text(self.window,'CREATE NEW CHARACTER',(0,0),isButton=False)
        text2 = Text(self.window,'ENTER CHARACTER NAME',(0,50),isButton=False)
        typeBar = TypeBar(self.window,(0,100),self.setPlayerName)
        text3 = Text(self.window,'SUBMIT',(0,150),isButton=True,menuAddress=self.createCharacter)
        text4 = Text(self.window,'BACK',(150,150),isButton=True,menuAddress=self.characterMenu)
        return Menu(self.window,self.cursor,text1,text2,text3,text4,typeBar)
    def worldMenu(self):
        text1 = Text(self.window,'WORLDS',(0,0),isButton=False)
        text2 = Text(self.window,'CREATE NEW WORLD',(0,50),isButton=True,menuAddress=self.worldCreationNameMenu)
        text3 = Text(self.window,'WORLD LIST',(0,100),isButton=True, menuAddress=True)
        text4 = Text(self.window,'BACK',(0,150),isButton=True,menuAddress=self.characterMenu)
        return Menu(self.window,self.cursor,text1,text2,text3,text4)
    def worldCreationNameMenu(self):
        text1 = Text(self.window,'CREATE NEW WORLD',(0,0),isButton=False)
        text2 = Text(self.window,'ENTER WORLD NAME',(0,50),isButton=False)
        typeBar = TypeBar(self.window,(0,100),self.setWorldName)
        text3 = Text(self.window,'SUBMIT',(0,150),isButton=True,menuAddress=self.worldCreationDifficultyMenu)
        text4 = Text(self.window,'BACK',(150,150),isButton=True,menuAddress=self.worldMenu)
        return Menu(self.window,self.cursor,text1,text2,text3,text4,typeBar)
    def worldCreationDifficultyMenu(self):
        text1 = Text(self.window,'CREATE NEW WORLD',(0,0),isButton=False)
        text2 = Text(self.window,'SELECT DIFFICULTY',(0,50),isButton=False)
        text3 = Text(self.window,'EASY',(0,100),isButton=True,menuAddress=self.easy)
        text4 = Text(self.window,'NORMAL',(100,100),isButton=True,menuAddress=self.normal)
        text5 = Text(self.window,'HARD',(200,100),isButton=True,menuAddress=self.hard)
        text6 = Text(self.window,'BACK',(150,150),isButton=True,menuAddress=self.worldMenu)
        return Menu(self.window,self.cursor,text1,text2,text3,text4,text5,text6)
        
    def update(self):
        runGame = False
        self.input.update()
        inputs = self.input.key
        menuAddress = self.currentMenu.update(inputs)
        
        if menuAddress != None:
            self.currentMenu = menuAddress()
        if self.currentMenu == 'exit':
            runGame = True
        self.cursor.update()
        #pygame.draw.rect(self.window.surface,(255,255,255),self.cursor.rect)
        return runGame


class TypeBar:
    def __init__(self,window,pos,setData):
        self.window = window
        self.rect = pygame.Rect(pos[0],pos[1],300,20)
        self.text = ''
        self.inputText = Text(self.window,'',(pos[0],pos[1]+2))
        self.setData = setData
    def update(self,inputs):
        if inputs != None:
            if inputs == 'backspace':
                self.text = self.text[:-1]
            else:
                self.text = self.text + inputs
        self.inputText.text = self.text
        self.inputText.textSurface = self.inputText.stringToSurface(self.text)
        self.inputText.update()
        self.setData(self.text)
        self.draw()
    def draw(self):
        pygame.draw.rect(self.window.GameSurface,(255,255,255),self.rect,1)


class Cursor():
    def __init__(self):
        self.rect = pygame.Rect(0,0,3,3)
        
        self.click = False

    @property
    def click(self):
        return self._click
    @click.setter
    def click(self,value):
        self._click = value

    def update(self):
        mx,my = pygame.mouse.get_pos()
        self.rect.x = mx/(700/300)
        self.rect.y = my/(500/200)
        self.click = False
    
class Text:
    def __init__(self,window,text,pos,letterImgsPath='assets/letters',isButton=False, menuAddress=None):
        self.window = window
        self.text = text
        self.pos = pos
        self.letters = self.getLetters(letterImgsPath)
        self.textSurface = self.stringToSurface(text)
        self.isbutton = isButton
        self.menuAddress = menuAddress
        if isButton:
            self.rect = pygame.Rect(self.pos[0],self.pos[1],len(text)*16,16)
            
    def stringToSurface(self,text):
        surf = pygame.Surface((len(text)*16,16))
        space = 0
        for i in range(len(text)):
            if text[i] == ' ':
                space -= 5
                continue
            surf.blit(self.letters[text[i].upper()],(i*9+space,0))
        return surf
    def update(self,cursorRect=None, inputs=False):
        if inputs:
            if self.isbutton:
                if cursorRect.colliderect(self.rect):
                    return self.menuAddress
        self.draw()
    def draw(self):
        self.window.GameSurface.blit(self.textSurface,self.pos)

    def getLetters(self,path):
        letters = {}
        for letter in string.ascii_letters[26:]:
            letters[letter] = pygame.image.load(path+'/'+letter+'.png')
        return letters


class Menu:
    def __init__(self,window,cursor,*argv):
        self.window = window
        self.text = []
        self.otherScreenObjects = []
        self.cursor = cursor
        for arg in argv:
            if isinstance(arg,Text):
                self.text.append(arg)
            else:
                self.otherScreenObjects.append(arg)
        
    def update(self, inputs):
        mouseInputs = inputs[1]
        keyboardInputs = inputs[0]
        for text in self.text:
            menuAddress = text.update(self.cursor.rect, mouseInputs)
            if menuAddress != None:
                return menuAddress
        for obj in self.otherScreenObjects:
            obj.update(keyboardInputs)
