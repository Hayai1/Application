import pygame, string,sys, os, random
from scripts.menuInput import MenuInput
from scripts.dbHandler import *

class Menu:#menu class
    def __init__(self,window,dbHandler,currentMenu):#constructor function for the menu class takes a window which is the surface to display everything on and a dbHandler to store and retrieve from the database
        self.window = window#window to display the menu on
        self.dbHandler = dbHandler#dbHandler to store and retrieve from the database
        self.cursor = Cursor(window)#cursor object
        self.input = MenuInput()#input object
        self.currentMenu = currentMenu()#current menu object
        self.click = False#is the mouse clicked

    def update(self):#update function
        self.input.update()#update the input
        inputs = self.input.input#inputs is a list of all the keys pressed
        menuAddress = self.currentMenu.update(inputs)#update the current menu and get the address of the next menu
        if menuAddress != None:#if the menu address is not none
            self.currentMenu = menuAddress()#set the current menu to the menu address
            if self.currentMenu == True:#if the current menu is true
                return True#return true
        self.cursor.update()#update the cursor
        return False#return false

class MainMenu(Menu):#main menu class
    def __init__(self,window,dbHandler):#constructor function for the main menu
        super().__init__(window, dbHandler, self.startMenu)#call the super constructor function with the start menu as the first menu to display
        self.playerId = None#player id
        self.playerName = None#player name
        self.worldName = None#world name
        self.worldDifficulty = None#world difficulty
        self.worldId = None#world id
    def setPlayerId(self,value):#set the player id
        self.playerId = value
    def setWorldId(self,value):#set the world id
        self.worldId = value#
    def setPlayerName(self,value):#set the player name
        self.playerName = value
    def setWorldName(self,value):#set the world name
        self.worldName = value
    #when difficulty is set all data is achieved hence the game will start
    def hard(self):#set the world difficulty to hard
        self.worldDifficulty = 3
        return self.createWorld()
    def normal(self):#set the world difficulty to normal
        self.worldDifficulty = 2
        return self.createWorld()
    def easy(self):#set the world difficulty to easy
        self.worldDifficulty = 1
        return self.createWorld()
    def createWorld(self):#create the world
        seed="5"#seed is a string of numbers which will be used to generate the world the first value is always 5
        roomAmount =50#the amount of rooms in the world
        for i in range(0,roomAmount-1):#for each room
            seed += str(random.randint(1,5))#add a random number between 1 and 5 to the seed
        self.worldId = self.dbHandler.createWorldRecord(self.worldName,self.worldDifficulty,seed)#create the world record in the database
        return self.exitMenu()#exit the menu
    def exitMenu(self):#exit the menu
        return True#return true
    def createCharacter(self):#create the character
        #create the character
        self.playerId = self.dbHandler.createCharacterRecord(self.playerName)#create the character record in the database and get this new characters id
        return self.worldMenu()#go to the world menu

    def getCharacterData(self):#get the character data
        players = self.dbHandler.getAllCharacterData()#get all the character data from the database
        return players#return the character data
    def getWorldData(self):
        worlds = self.dbHandler.getAllWorldData()#get all the world data from the database
        return worlds#return the world data
    

        

    def startMenu(self):#start menu
        text1 = Text(self.window.GameSurface,'GAME NAME',(0,0),isButton=False)#create a text object with the text GAME NAME
        text2 = Text(self.window.GameSurface,'START',(0,50),isButton=True,menuAddress=self.characterMenu)#create a text object with the text START
        text3 = Text(self.window.GameSurface,'EXIT',(0,100),isButton=True,menuAddress=sys.exit)#create a text object with the text EXIT
        return MenuScreen(self.window,self.cursor,text1,text2,text3)#return a menu screen object with the text objects
        
    def characterMenu(self):#character menu
        text1 = Text(self.window.GameSurface,'CHARACTERS',(0,0),isButton=False)#create a text object with the text CHARACTERS
        text2 = Text(self.window.GameSurface,'CREATE NEW CHARACTER',(0,50),isButton=True,menuAddress=self.characterCreationMenuEnterName)#create a text object with the text CREATE NEW CHARACTER
        text3 = Text(self.window.GameSurface,'CHARACTER LIST',(0,100),isButton=True,menuAddress=self.characterLoadMenu)#create a text object with the text CHARACTER LIST
        text4 = Text(self.window.GameSurface,'BACK',(0,150),isButton=True,menuAddress=self.startMenu)#create a text object with the text BACK
        return MenuScreen(self.window,self.cursor,text1,text2,text3,text4)#return a menu screen object with the text objects
    def characterLoadMenu(self):
        text1 = Text(self.window.GameSurface,'LOAD CHARACTER',(0,0),isButton=False)#create a text object with the text LOAD CHARACTER
        text2 = Text(self.window.GameSurface,'SUBMIT',(200,50),isButton=True,menuAddress=self.worldMenu)#create a text object with the text SUBMIT
        text3 = Text(self.window.GameSurface,'BACK',(200,150),isButton=True,menuAddress=self.characterMenu)#create a text object with the text BACK
        list1 = ListBox(self.window,(25,25),150,150,self.getCharacterData(),self.cursor,self.setPlayerId)#create a list box object with the character data
        return MenuScreen(self.window,self.cursor,text2,text3,text1,list1)#return a menu screen object with the text objects and the list box object
    def characterCreationMenuEnterName(self):#character creation menu enter name
        text1 = Text(self.window.GameSurface,'CREATE NEW CHARACTER',(0,0),isButton=False)#create a text object with the text CREATE NEW CHARACTER
        text2 = Text(self.window.GameSurface,'ENTER CHARACTER NAME',(0,50),isButton=False)#create a text object with the text ENTER CHARACTER NAME
        typeBar = TypeBar(self.window.GameSurface,(0,100),self.setPlayerName)#create a type bar object with the set player name function
        text3 = Text(self.window.GameSurface,'SUBMIT',(0,150),isButton=True,menuAddress=self.createCharacter)#create a text object with the text SUBMIT
        text4 = Text(self.window.GameSurface,'BACK',(150,150),isButton=True,menuAddress=self.characterMenu)#create a text object with the text BACK
        return MenuScreen(self.window.GameSurface,self.cursor,text1,text2,text3,text4,typeBar)#return a menu screen object with the text objects and the type bar object
    def worldMenu(self):#world menu
        text1 = Text(self.window.GameSurface,'WORLDS',(0,0),isButton=False)#create a text object with the text WORLDS
        text2 = Text(self.window.GameSurface,'CREATE NEW WORLD',(0,50),isButton=True,menuAddress=self.worldCreationNameMenu)#create a text object with the text CREATE NEW WORLD
        text3 = Text(self.window.GameSurface,'WORLD LIST',(0,100),isButton=True, menuAddress=self.worldLoadMenu)#create a text object with the text WORLD LIST
        text4 = Text(self.window.GameSurface,'BACK',(0,150),isButton=True,menuAddress=self.characterMenu)#create a text object with the text BACK
        return MenuScreen(self.window.GameSurface,self.cursor,text1,text2,text3,text4)#return a menu screen object with the text objects
    def worldLoadMenu(self):#world load menu
        text1 = Text(self.window.GameSurface,'LOAD WORLD',(0,0),isButton=False)#create a text object with the text LOAD WORLD
        text2 = Text(self.window.GameSurface,'SUBMIT',(200,50),isButton=True,menuAddress=self.exitMenu)#create a text object with the text SUBMIT
        text3 = Text(self.window.GameSurface,'BACK',(200,150),isButton=True,menuAddress=self.worldMenu)#create a text object with the text BACK
        list1 = ListBox(self.window,(25,25),150,150,self.getWorldData(),self.cursor,self.setWorldId)#create a list box object with the world data
        return MenuScreen(self.window.GameSurface,self.cursor,text2,text3,text1,list1)#return a menu screen object with the text objects and the list box object
    def worldCreationNameMenu(self): #world creation menu enter name
        text1 = Text(self.window.GameSurface,'CREATE NEW WORLD',(0,0),isButton=False)#create a text object with the text CREATE NEW WORLD
        text2 = Text(self.window.GameSurface,'ENTER WORLD NAME',(0,50),isButton=False)#create a text object with the text ENTER WORLD NAME
        typeBar = TypeBar(self.window.GameSurface,(0,100),self.setWorldName)#create a type bar object with the set world name function
        text3 = Text(self.window.GameSurface,'SUBMIT',(0,150),isButton=True,menuAddress=self.worldCreationDifficultyMenu)#create a text object with the text SUBMIT
        text4 = Text(self.window.GameSurface,'BACK',(150,150),isButton=True,menuAddress=self.worldMenu)#create a text object with the text BACK
        return MenuScreen(self.window.GameSurface,self.cursor,text1,text2,text3,text4,typeBar)#return a menu screen object with the text objects and the type bar object
    def worldCreationDifficultyMenu(self):#world creation menu difficulty
        text1 = Text(self.window.GameSurface,'CREATE NEW WORLD',(0,0),isButton=False)#create a text object with the text CREATE NEW WORLD
        text2 = Text(self.window.GameSurface,'SELECT DIFFICULTY',(0,50),isButton=False)#create a text object with the text SELECT DIFFICULTY
        text3 = Text(self.window.GameSurface,'EASY',(0,100),isButton=True,menuAddress=self.easy)#create a text object with the text EASY
        text4 = Text(self.window.GameSurface,'NORMAL',(100,100),isButton=True,menuAddress=self.normal)#create a text object with the text NORMAL
        text5 = Text(self.window.GameSurface,'HARD',(200,100),isButton=True,menuAddress=self.hard)#create a text object with the text HARD
        text6 = Text(self.window.GameSurface,'BACK',(150,150),isButton=True,menuAddress=self.worldMenu)#create a text object with the text BACK
        return MenuScreen(self.window,self.cursor,text1,text2,text3,text4,text5,text6)#return a menu screen object with the text objects
        
    
class ListBox:#list box class
    def __init__(self,window, pos,width,height,players,cursor,setIdFuntion):#list box constructor
        self.window = window #window
        self.pos = pos#position
        self.cursorRect = cursor.rect#cursor rect
        self.setIdFuntion=setIdFuntion#set id function
        self.scrollAmount = 0#amount to push up or down data in list box
        self.rect = pygame.Rect(pos[0],pos[1],width,height)#rect
        self.contentsSurf = pygame.Surface((width,height))#contents surface
        self.elements = self.mergeSort(self.getElements(players,width))#elements
    
    def mergeSort(self,elements):#merge sort function
        if len(elements) > 1:#if the length of the elements is greater than 1
            mid = len(elements)//2#mid is the length of the elements divided by 2
            left = elements[:mid]#left is the elements from 0 to mid
            right = elements[mid:]#right is the elements from mid to the end
            self.mergeSort(left)#merge sort left
            self.mergeSort(right)#merge sort right
            i = 0#i is 0
            j = 0#j is 0
            k = 0#k is 0
            while i < len(left) and j < len(right):#while i is less than the length of left and j is less than the length of right
                if left[i]['name'] < right[j]['name']:#if the name of left at i is less than the name of right at j
                    elements[k] = left[i]#elements at k is left at i
                    i += 1#i is i plus 1
                else:
                    elements[k] = right[j]#elements at k is right at j
                    j += 1#j is j plus 1
                k += 1#k is k plus 1
            while i < len(left):#while i is less than the length of left
                elements[k] = left[i]#elements at k is left at i
                i += 1# i plus 1
                k += 1#k plus 1
            while j < len(right):#while j is less than the length of right
                elements[k] = right[j]#elements at k is right at j
                j += 1#j plus 1
                k += 1#k plus 1
        return elements#return elements

    def getElements(self,players,width):#get elements function returns a list of dictionaries which contain data on the players and the box to display
        elements = []#elements is an empty list
        for player in players:#for each player in players
            surf = pygame.Surface((width,32))#surf is a surface with the width and height of 32
            rect = pygame.Rect(0,0,width,32)#rect is a rect with the width and height of 32
            text = Text(surf,player[1].upper(),[5,5],letterImgsPath='assets/letters')#text is a text object with the text being the name of the player
            box = {#box is a dictionary with the following keys and values
                "id" : player[0],#id is the id of the player
                "name" : player[1],#name is the name of the player
                "nameRender" : text,#nameRender is the text object
                "surf" : surf,#surf is the surface
                "rect" : rect,#rect is the rect
                "color" : (0,0,0)#color is black
            }
            elements.append(box)#append box to elements
        return elements#return elements

    def update(self,input):#update function takes an input 
        self.cursorRect.x = self.cursorRect.x - self.pos[0]#centre cursor rect onto the mouse when in the list box
        self.cursorRect.y = self.cursorRect.y - self.pos[1]#centre cursor rect onto the mouse when in the list box
        if input == 1:#if the user clicks 
            for box in self.elements:#for each box in elements
                box["color"] = (0,0,0)#set the color of the box to black
                if self.cursorRect.colliderect(box["rect"]):#if the cursor is hovering over box['rect]
                    box["color"] = (255,0,0)#set the color of the box to red
                    self.setIdFuntion(box["id"])#set the id of the player to the id of the box
        #if the user scrolls elements in the list box should go up or down
        elif input == 5 and not self.elements[-1]["rect"].y < self.rect.height-32:#if the user scrolls up and the last element is not at the bottom of the list box
            self.scrollAmount -= 5#decrease the scrollAmount by 5 so the elements go up
        elif input == 4 and not self.elements[0]["rect"].y == 0:#if the user presses down and the first element is not at the top of the list box
            self.scrollAmount += 5#increase the scrollAmount by 5 so the elements go down
        self.contentsSurf.fill((0,0,0))#fill the contents surface with black
        y = 0
        for element in self.elements:#for each element in elements
            surf = element["surf"]#surf is the surface of the element
            rect = element["rect"]#rect is the rect of the element
            text = element["nameRender"]#text is the text object of the element
            rect.y = 0#set the y of the rect to 0
            rect.y = rect.y+(38*y)#set the y of the rect to the default position by adding each elements y location to by 38y we x38 as the height of the rect is 32 and we want a gap of 6 between each element
            rect.y += self.scrollAmount#add the scrollAmount to the y of the rect so the elements move up and down
            surf.fill(element["color"])#fill the surface with the color of the element
            text.update()#update the text object
            self.contentsSurf.blit(surf, (rect.x,rect.y))#blit the surface to the contents surface
            pygame.draw.rect(self.contentsSurf, (0,0,0), rect,1)#draw a black rect around the surface
            y+=1#increase y by 1 so the next element is drawn below the previous element
        
        self.window.GameSurface.blit(self.contentsSurf, (self.pos))#blit the contents surface to the window surface
        pygame.draw.rect(self.window.GameSurface, (255,255,255), self.rect,1)#draw a white rect around the list box
        
        



class TypeBar:#type bar class
    def __init__(self,window,pos,setData):#takes a window, a position and a setData function
        self.window = window#set the window to the window
        self.rect = pygame.Rect(pos[0],pos[1],300,20)#set the rect to a rect with the position and the width and height of 300 and 20
        self.text = ''#set the text to an empty string
        self.inputText = Text(self.window,'',(pos[0],pos[1]+2))#set the inputText to a text object with the text being an empty string and the position being the position of the type bar
        self.setData = setData#set the setData function to the setData function
    def update(self,inputs):#update function takes an input
        if inputs != None:#if the input is not none
            if inputs == 'backspace':#if the input is backspace
                self.text = self.text[:-1]#remove the last character from the text
            else:#if the input is not backspace
                self.text = self.text + inputs#add the input to the text
        self.inputText.text = self.text#set the text of the inputText to the text
        self.inputText.textSurface = self.inputText.stringToSurface(self.text)#create a new text surface with the added text
        self.inputText.update()#update the inputText
        self.setData(self.text)#set the data of the type bar to the text
        self.draw()#draw the type bar
    def draw(self):#draw function
        pygame.draw.rect(self.window,(255,255,255),self.rect,1)#draw a white rect around the type bar


class Cursor():#cursor class
    def __init__(self,window):#takes a window
        self.rect = pygame.Rect(0,0,3,3)#set the rect to a rect with the position and the width and height of 3 and 3
        self.window = window#set the window to the window
        self.click = False#set the click to false

    @property
    def click(self):#get the click
        return self._click
    @click.setter#set the click
    def click(self,value):#takes a value
        self._click = value

    def update(self):#update function
        mx,my = pygame.mouse.get_pos()#get the position of the mouse
        self.rect.x = mx/(self.window.screen.get_width()/300)#set the x of the rect to the x of the mouse divided by the width of the screen divided by 300
        self.rect.y = my/(self.window.screen.get_height()/200)#set the y of the rect to the y of the mouse divided by the height of the screen divided by 200
        self.click = False#set the click to false
    
class Text:
    def __init__(self,window,text,pos,letterImgsPath='assets/letters',isButton=False, menuAddress=None):#takes a window, a text, a position, a letterImgsPath, a isButton and a menuAddress
        self.window = window#set the window to the window
        self.text = text#set the text to the text
        self.pos = pos#set the pos to the pos
        self.letters = self.getLetters(letterImgsPath)#get the letters at the letterImgsPath
        self.textSurface = self.stringToSurface(text)#get the text surface
        self.isbutton = isButton#text can be a button or it can just be text
        self.menuAddress = menuAddress#set the menuAddress to the menuAddress
        if isButton:#if the text is a button
            self.rect = pygame.Rect(self.pos[0],self.pos[1],len(text)*9,16)#give the text a rect so it can deal with collisions
            
    def stringToSurface(self,text):#takes a string and returns a surface with the string on it
        surf = pygame.Surface((len(text)*16,16))#create a surface with the width of the string times 16 and the height of 16
        space = 0
        i = 0
        for letter in text:#for each letter in the string
            
            if letter == ' ':#if the letter is a space
                space += 5#add 5 to the space
                continue#get next letter in text
            else:#if the letter is not a space
                try: #try to blit the letter to the surface
                    (surf.blit(self.letters[letter.upper()],(i*9+space,0)))#blit the letter to the surface
                except:#if the letter is not in the letters dict
                    i-=1#decrease i by 1 so the next letter is not drawn in the same place as the previous letter
            i+=1#increase i by 1 so the next letter is drawn to the right of the previous letter
        return surf#return the surface
    def update(self,cursorRect=None, inputs=False):#update function
        if inputs and self.isbutton and cursorRect.colliderect(self.rect):#if the user has clicked and the text is a button and the cursor is colliding with the text
            return self.menuAddress#return the pointer to the next menu screen
        self.draw()#draw the text
    def draw(self):#draw function
        self.window.blit(self.textSurface,self.pos)#blit the text surface to the window at the position
        

    def getLetters(self,path):#takes a path and returns a dict with the letters as keys and the images as values
        letters = {}#create a dict
        for letter in string.ascii_letters[26:]:#for each letter in the alphabet
            letters[letter] = pygame.image.load(path+'/'+letter+'.png')#add the letter to the dict with the image of the letter
        return letters#return the dict


class MenuScreen:
    def __init__(self,window,cursor,*argv):#takes a window, a cursor and any number of other objects that are on the screen (text, typebars, listboxes)
        self.window = window#set the window to the window
        self.text = []#create a list for the text
        self.typeBars = []#create a list for the typebars
        self.listBoxes = []#create a list for the listboxes
        self.otherScreenObjects = []#create a list for other objects
        self.cursor = cursor#set the cursor to the cursor
        for arg in argv:#for each object
            if isinstance(arg,Text):#if the object is text
                self.text.append(arg)#add the text to the text list
            elif isinstance(arg,TypeBar):#if the object is a typebar
                self.typeBars.append(arg)#add the typebar to the typebar list
            elif isinstance(arg,ListBox):#if the object is a listbox
                self.listBoxes.append(arg)#add the listbox to the listbox list
            else:#if the object is not text, typebar or listbox
                self.otherScreenObjects.append(arg)#add the object to the other objects list
        
    def update(self, inputs):#takes the inputs and updates the screen
        mouseInputs = inputs[1]#get the mouse inputs
        keyboardInputs = inputs[0]#get the keyboard inputs
        for text in self.text:#for each text
            menuAddress = text.update(self.cursor.rect, mouseInputs==1)#update the text and get the menu address
            if menuAddress != None:#if the menu address is not none
                return menuAddress#return the menu address
        for typeBar in self.typeBars:#for each typebar
            typeBar.update(keyboardInputs)#update the typebar
        for listBox in self.listBoxes:#for each listbox
            listBox.update(mouseInputs)#update the listbox
