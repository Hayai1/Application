import pygame, string,sys, os, random
from scripts.menuInput import MenuInput
from scripts.dbHandler import *

class Menu:
    def __init__(self,window,dbHandler,currentMenu):
        self.window = window
        self.dbHandler = dbHandler
        self.cursor = Cursor(window)
        self.input = MenuInput()
        self.currentMenu = currentMenu()
        self.click = False

    def update(self):
        self.input.update()
        inputs = self.input.key
        menuAddress = self.currentMenu.update(inputs)
        if menuAddress != None:
            self.currentMenu = menuAddress()
            if self.currentMenu == True:
                return True
        self.cursor.update()
        return False

class MainMenu(Menu):
    def __init__(self,window,dbHandler):
        super().__init__(window, dbHandler, self.startMenu)

        self.playerId = None
        self.playerName = None
        self.worldName = None
        self.worldDifficulty = None
        self.playerId = None
        self.worldId = None
        self.newWorld = False
        self.newPlayer = False
    def setPlayerId(self,value):
        self.playerId = value
    def setWorldId(self,value):
        self.worldId = value
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
        seed="5"
        roomAmount =50
        for i in range(0,roomAmount-1):
            seed += str(random.randint(1,5))
        self.worldId = self.dbHandler.createWorldRecord(self.worldName,self.worldDifficulty,seed)
        self.newWorld = True
        return self.exitMenu()
    def exitMenu(self):
        if self.newWorld == True or self.newPlayer == True:
            self.dbHandler.newCharacterPositionsRecord()
        return True
    def createCharacter(self):
        #create the character
        self.playerId = self.dbHandler.createCharacterRecord(self.playerName)
        self.newPlayer = True
        return self.worldMenu()

    def getCharacterData(self):
        players = self.dbHandler.getAllCharacterData()
        return players
    def getWorldData(self):
        worlds = self.dbHandler.getAllWorldData()
        return worlds
    

        

    def startMenu(self):
        text1 = Text(self.window.GameSurface,'GAME NAME',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'START',(0,50),isButton=True,menuAddress=self.characterMenu)
        text3 = Text(self.window.GameSurface,'EXIT',(0,100),isButton=True,menuAddress=sys.exit)
        return MenuScreen(self.window,self.cursor,text1,text2,text3)
        
    def characterMenu(self):
        text1 = Text(self.window.GameSurface,'CHARACTERS',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'CREATE NEW CHARACTER',(0,50),isButton=True,menuAddress=self.characterCreationMenuEnterName)
        text3 = Text(self.window.GameSurface,'CHARACTER LIST',(0,100),isButton=True,menuAddress=self.characterLoadMenu)
        text4 = Text(self.window.GameSurface,'BACK',(0,150),isButton=True,menuAddress=self.startMenu)
        return MenuScreen(self.window,self.cursor,text1,text2,text3,text4)
    def characterLoadMenu(self):
        text1 = Text(self.window.GameSurface,'LOAD CHARACTER',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'SUBMIT',(200,50),isButton=True,menuAddress=self.worldMenu)
        text3 = Text(self.window.GameSurface,'BACK',(200,150),isButton=True,menuAddress=self.characterMenu)
        list1 = ListBox(self.window,(25,25),150,150,self.getCharacterData(),self.cursor,self.setPlayerId)
        return MenuScreen(self.window,self.cursor,text2,text3,text1,list1)
    def characterCreationMenuEnterName(self):
        text1 = Text(self.window.GameSurface,'CREATE NEW CHARACTER',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'ENTER CHARACTER NAME',(0,50),isButton=False)
        typeBar = TypeBar(self.window.GameSurface,(0,100),self.setPlayerName)
        text3 = Text(self.window.GameSurface,'SUBMIT',(0,150),isButton=True,menuAddress=self.createCharacter)
        text4 = Text(self.window.GameSurface,'BACK',(150,150),isButton=True,menuAddress=self.characterMenu)
        return MenuScreen(self.window.GameSurface,self.cursor,text1,text2,text3,text4,typeBar)
    def worldMenu(self):
        text1 = Text(self.window.GameSurface,'WORLDS',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'CREATE NEW WORLD',(0,50),isButton=True,menuAddress=self.worldCreationNameMenu)
        text3 = Text(self.window.GameSurface,'WORLD LIST',(0,100),isButton=True, menuAddress=self.worldLoadMenu)
        text4 = Text(self.window.GameSurface,'BACK',(0,150),isButton=True,menuAddress=self.characterMenu)
        return MenuScreen(self.window.GameSurface,self.cursor,text1,text2,text3,text4)
    def worldLoadMenu(self):
        text1 = Text(self.window.GameSurface,'LOAD WORLD',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'SUBMIT',(200,50),isButton=True,menuAddress=self.exitMenu)
        text3 = Text(self.window.GameSurface,'BACK',(200,150),isButton=True,menuAddress=self.worldMenu)
        list1 = ListBox(self.window,(25,25),150,150,self.getWorldData(),self.cursor,self.setWorldId)
        return MenuScreen(self.window.GameSurface,self.cursor,text2,text3,text1,list1)
    def worldCreationNameMenu(self): 
        text1 = Text(self.window.GameSurface,'CREATE NEW WORLD',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'ENTER WORLD NAME',(0,50),isButton=False)
        typeBar = TypeBar(self.window.GameSurface,(0,100),self.setWorldName)
        text3 = Text(self.window.GameSurface,'SUBMIT',(0,150),isButton=True,menuAddress=self.worldCreationDifficultyMenu)
        text4 = Text(self.window.GameSurface,'BACK',(150,150),isButton=True,menuAddress=self.worldMenu)
        return MenuScreen(self.window.GameSurface,self.cursor,text1,text2,text3,text4,typeBar)
    def worldCreationDifficultyMenu(self):
        text1 = Text(self.window.GameSurface,'CREATE NEW WORLD',(0,0),isButton=False)
        text2 = Text(self.window.GameSurface,'SELECT DIFFICULTY',(0,50),isButton=False)
        text3 = Text(self.window.GameSurface,'EASY',(0,100),isButton=True,menuAddress=self.easy)
        text4 = Text(self.window.GameSurface,'NORMAL',(100,100),isButton=True,menuAddress=self.normal)
        text5 = Text(self.window.GameSurface,'HARD',(200,100),isButton=True,menuAddress=self.hard)
        text6 = Text(self.window.GameSurface,'BACK',(150,150),isButton=True,menuAddress=self.worldMenu)
        return MenuScreen(self.window,self.cursor,text1,text2,text3,text4,text5,text6)
        
    
class ListBox:
    def __init__(self,window, pos,width,height,players,cursor,setIdFuntion):
        self.window = window 
        self.pos = pos
        self.cursorRect = cursor.rect
        self.setIdFuntion=setIdFuntion
        self.counter = 0
        self.rect = pygame.Rect(pos[0],pos[1],width,height)
        self.contentsSurf = pygame.Surface((width,height))
        self.elements = self.mergeSort(self.getElements(players,width))
    
    def mergeSort(self,elements):
        if len(elements) > 1:
            mid = len(elements)//2
            left = elements[:mid]
            right = elements[mid:]
            self.mergeSort(left)
            self.mergeSort(right)
            i = 0
            j = 0
            k = 0
            while i < len(left) and j < len(right):
                if left[i]['name'] < right[j]['name']:
                    elements[k] = left[i]
                    i += 1
                else:
                    elements[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                elements[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                elements[k] = right[j]
                j += 1
                k += 1
        return elements
    
    



    def getElements(self,players,width):
        elements = []
        for player in players:
            surf = pygame.Surface((width,32))
            rect = pygame.Rect(0,0,width,32)
            text = Text(surf,player[1].upper(),[5,5],letterImgsPath='assets/letters')
            box = {
                "id" : player[0],
                "name" : player[1],
                "nameRender" : text,
                "surf" : surf,
                "rect" : rect,
                "color" : (0,0,0)
            }
            elements.append(box)
        return elements

    def update(self,input):
        self.cursorRect.x = self.cursorRect.x - self.pos[0]#centre cursor rect onto the mouse
        self.cursorRect.y = self.cursorRect.y - self.pos[1]
        if input == 1:
            for box in self.elements:
                box["color"] = (0,0,0)                
                if self.cursorRect.colliderect(box["rect"]):
                    box["color"] = (255,0,0)
                    self.setIdFuntion(box["id"])
        elif input == 5 and not self.elements[-1]["rect"].y < self.rect.height-32:
            self.counter -= 5
        elif input == 4 and not self.elements[0]["rect"].y == 0:
            self.counter += 5
        self.contentsSurf.fill((0,0,0))
        y = 0
        for element in self.elements:
            surf = element["surf"]
            rect = element["rect"]
            text = element["nameRender"]
            
            rect.y = 0
            
            rect.y = rect.y+(38*y)+ self.counter
            
            
            
            surf.fill(element["color"])
            text.update()
            self.contentsSurf.blit(surf, (rect.x,rect.y))
            pygame.draw.rect(self.contentsSurf, (0,0,0), rect,1)
            y+=1
        
        self.window.GameSurface.blit(self.contentsSurf, (self.pos))
        pygame.draw.rect(self.window.GameSurface, (255,255,255), self.rect,1)
        
        



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
        pygame.draw.rect(self.window,(255,255,255),self.rect,1)


class Cursor():
    def __init__(self,window):
        self.rect = pygame.Rect(0,0,3,3)
        self.window = window
        self.click = False

    @property
    def click(self):
        return self._click
    @click.setter
    def click(self,value):
        self._click = value

    def update(self):
        mx,my = pygame.mouse.get_pos()
        self.rect.x = mx/(self.window.screen.get_width()/300)
        self.rect.y = my/(self.window.screen.get_height()/200)
        pygame.draw.rect(self.window.GameSurface,(255,255,255),self.rect)
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
        self.window.blit(self.textSurface,self.pos)

    def getLetters(self,path):
        letters = {}
        for letter in string.ascii_letters[26:]:
            letters[letter] = pygame.image.load(path+'/'+letter+'.png')
        return letters


class MenuScreen:
    def __init__(self,window,cursor,*argv):
        self.window = window
        self.text = []
        self.typeBars = []
        self.listBoxes = []
        self.otherScreenObjects = []
        self.cursor = cursor
        for arg in argv:
            if isinstance(arg,Text):
                self.text.append(arg)
            elif isinstance(arg,TypeBar):
                self.typeBars.append(arg)
            elif isinstance(arg,ListBox):
                self.listBoxes.append(arg)
            else:
                self.otherScreenObjects.append(arg)
        
    def update(self, inputs):
        mouseInputs = inputs[1]
        keyboardInputs = inputs[0]
        for text in self.text:
            menuAddress = text.update(self.cursor.rect, mouseInputs==1)
            if menuAddress != None:
                return menuAddress
        for typeBar in self.typeBars:
            typeBar.update(keyboardInputs)
        for listBox in self.listBoxes:
            listBox.update(mouseInputs)
