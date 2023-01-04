import pygame, string,sys
from scripts.menuInput import MenuInput

class MenuManager:
    def __init__(self,window):
        self.window = window
        self.currentMenu = self.menu1
        self.cursor = Cursor()
        self.click = False
    

    def menu1(self):
        text1 = Text(self.window,'GAME NAME',(0,0),isButton=False)
        text2 = Text(self.window,'START',(0,50),isButton=True,menuAddress=self.menu2)
        text3 = Text(self.window,'EXIT',(0,100),isButton=True,menuAddress=sys.exit)
        return Menu(self.window,self.cursor,text1,text2,text3)
    def menu2(self):
        text1 = Text(self.window,'CHARACTERS',(0,0),isButton=False)
        text2 = Text(self.window,'CREATE NEW CHARACTER',(0,50),isButton=True,menuAddress=self.menu3)
        text3 = Text(self.window,'CHARACTER LIST',(0,100),isButton=True,menuAddress=self.menu3)
        text4 = Text(self.window,'BACK',(0,150),isButton=True,menuAddress=self.menu1)
        return Menu(self.window,self.cursor,text1,text2,text3,text4)
    def menu3(self):
        text1 = Text(self.window,'WORLDS',(0,0),isButton=False)
        text2 = Text(self.window,'CREATE NEW WORLD',(0,50),isButton=True,menuAddress=True)
        text3 = Text(self.window,'WORLD LIST',(0,100),isButton=True, menuAddress=True)
        text4 = Text(self.window,'BACK',(0,150),isButton=True,menuAddress=self.menu2)
        return Menu(self.window,self.cursor,text1,text2,text3,text4)
        
    def update(self):
        runGame = False
        inputs = self.cursor.getInput()
        menuAddress = self.currentMenu().update(inputs)
        if menuAddress == True:
            runGame = True
        elif menuAddress != None:
            self.currentMenu = menuAddress
        self.cursor.update()
        pygame.draw.rect(self.window.surface,(255,255,255),self.cursor.rect)
        return runGame

 
class Cursor():
    def __init__(self):
        self.rect = pygame.Rect(0,0,16,16)
        self.input = MenuInput(self)
        self.click = False

    @property
    def click(self):
        return self._click
    @click.setter
    def click(self,value):
        self._click = value
    def getInput(self):
        self.input.update()
        return self.click 

    def update(self):
        mx,my = pygame.mouse.get_pos()
        self.rect.x = mx/(700/300)
        self.rect.y = my/(500/200)
        self.click = False
    


class Menu:
    def __init__(self,window,cursor,*argv):
        self.window = window
        self.text = []
        self.cursor = cursor
        for arg in argv:
            self.text.append(arg)
        
    def update(self, inputs):
        for text in self.text:
            menuAddress = text.update(self.cursor.rect, inputs)
            if menuAddress != None:
                return menuAddress
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
        for i in range(len(text)):
            if text[i] == ' ':
                continue
            surf.blit(self.letters[text[i]],(i*16,0))
        return surf
    def update(self,cursorRect, inputs):
        if self.isbutton and inputs:
            if cursorRect.colliderect(self.rect):
                return self.menuAddress
        self.draw()
    def draw(self):
        self.window.surface.blit(self.textSurface,self.pos)

    def getLetters(self,path):
        letters = {}
        for letter in string.ascii_letters[26:]:
            letters[letter] = pygame.image.load(path+'/'+letter+'.png')
        return letters
