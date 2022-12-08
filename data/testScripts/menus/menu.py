import pygame
import string
class Menu():
    def __init__(self,id):
        self.id = id
        self.menu = {'buttons' : [],'textBoxes' : [],'typebars' : [],}
        self.typing=False

    def createTextBox(self,LetterPath,ID,text,x,y,lettersPerLine,menuPointer=None):
        textBox = self.TextBox(LetterPath,ID,text,x,y,lettersPerLine,menuPointer)
        self.menu['textBoxes'].append(textBox)
        return textBox
    def createButton(self,id, imgPath, x,y,menuPointer):
        button = self.Button(id, imgPath, x,y,menuPointer)
        self.menu['buttons'].append(button)
        return button
    def createTypeBar(self,x,y,imgPath=None,width=400,height=50):
        typebar = self.TypeBar(x,y,imgPath,width,height)
        self.menu['typebars'].append(typebar)
        return typebar


    def checkForButtonUpdates(self,currentMenu,button,cursor):
        if button.pointer is not None and cursor.rect.colliderect(button.rect):
            button.hover = True
            if cursor.click:
                cursor.click = False
                if button.pointer != None:
                    return button.pressButton()
        else:
            button.hover = False
        return currentMenu
    def update(self,screen,cursor):
        currentMenu = self
        for textbox in self.menu['textBoxes']:
            if textbox.pointer is not None:
                currentMenu = self.checkForButtonUpdates(currentMenu,textbox,cursor)
        for button in self.menu['buttons']:
            currentMenu = self.checkForButtonUpdates(currentMenu,button,cursor)
        for typebar in self.menu['typebars']:
            self.typing = self.checkForButtonUpdates(currentMenu,typebar,cursor)
            
        cursor.click = False
        if currentMenu != self:
            self.typing = False
        #draw the menu
        for textbox in self.menu['textBoxes']:
            textbox.draw(screen)
        for button in self.menu['buttons']:
            button.draw(screen)
        for typebar in self.menu['typebars']:
            typebar.draw(screen)
        return currentMenu
    def typeLetter(self,key):
        for typebar in self.menu['typebars']:
            if typebar.using:
                typebar.typeLetter(key)
    class TypeBar:
        def __init__(self,x, y,imgPath=None, width=100, height=20,letterPath='assets/letters/'):
            self.img = imgPath
            self.pointer = 'typing'
            self.using = False
            self.data = ''
            switch = {
                pygame.K_a : 'a',
                pygame.K_b : 'b',
                pygame.K_c : 'c',
                pygame.K_d : 'd',
                pygame.K_e : 'e',
                pygame.K_f : 'f',
                pygame.K_g : 'g',
                pygame.K_h : 'h',
                pygame.K_i : 'i',
                pygame.K_j : 'j',
                pygame.K_k : 'k',
                pygame.K_l : 'l',
                pygame.K_m : 'm',
                pygame.K_n : 'n',
                pygame.K_o : 'o',
                pygame.K_p : 'p',
                pygame.K_q : 'q',
                pygame.K_r : 'r',
                pygame.K_s : 's',
                pygame.K_t : 't',
                pygame.K_u : 'u',
                pygame.K_v : 'v',
                pygame.K_w : 'w',
                pygame.K_x : 'x',
                pygame.K_y : 'y',
                pygame.K_z : 'z',
                pygame.K_SPACE : ' ',
            }
            if self.img is None:
                self.width = width
                self.height = height
                self.rect = pygame.Rect(x,y,width,height)
            elif self.img is not None:
                self.img = pygame.image.load(imgPath)
                self.rect = pygame.Rect(x,y,self.img.get_width(),self.img.get_height())
            self.textInTypeBar = Menu.TextBox(letterPath,'',self.data,self.x,self.y,20)
            
        def typeLetter(self,key):
            if key == pygame.K_BACKSPACE:
                self.data = self.data[:-1]
            else:
                self.data += key
            
        @property
        def x(self):
            return self.rect.x
        @x.setter
        def x(self, value):
            self.rect.x = value
        @property
        def y(self):
            return self.rect.y
        @y.setter
        def y(self, value):
            self.rect.y = value
        
        def draw(self,screen):
            if self.img is not None:
                return screen.blit(self.img, (self.x-self.width/2, self.y-self.height/2))
            elif self.img is None:
                pygame.draw.rect(screen, (255, 255, 255), (self.x-self.width/2,self.y-self.height,self.width,self.height), 1)
            self.textInTypeBar.text += 
            self.textInTypeBar.surf, self.textInTypeBar.size = self.textInTypeBar.getTextBox()
            self.textInTypeBar.draw(screen)
                
        def pressButton(self):
            self.useing = True
            return self.typing
    class Button:
        def __init__(self,imgPath,id,x,y,pointer):
            self.id = id
            self.img = self.getImg(imgPath)
            self.pointer = pointer
            self.hover = False
            self.rect = pygame.Rect(x, y, self.width, self.height)
            
        def getImg(self,path):
            return pygame.image.load(path)
        @property
        def width(self):
            return self.img.get_width()
        @property
        def height(self):
            return self.img.get_height()
        @property
        def x(self):
            return self.rect.x
        @x.setter
        def x(self,value):
            self.rect.x = value
        @property
        def y(self):
            return self.rect.y
        def draw(self,screen):
            screen.blit(self.img, (self.x-self.width/2, self.y-self.height/2))
        def pressButton(self):
            if type(self.pointer) is str and self.pointer.Upper() is 'QUIT':
                pygame.quit()
                quit()
            elif type(self.pointer) is Menu:
                return self.pointer
            
        
    class TextBox:
        def __init__(self,path,ID,text,x=0,y=0,lettersPerLine=30,menuPointer = None):
            self.ID = ID
            self.path = path
            self.letters = self.getLetters()
            self.textBoxes = {}
            self.text= text
            self.lettersPerLine = lettersPerLine
            self.img,self.size = self.getTextBox()
            self.rect =None
            self.rect = pygame.Rect(x,y,self.size[0],self.size[1])
            self.pointer = menuPointer
        @property
        def x(self):
            return self.rect.x
        @x.setter
        def x(self,x):
            self.rect.x = x
        @property
        def y(self):
            return self.rect.y
        @y.setter
        def y(self,y):
            self.rect.y = y
        def pressButton(self):
            if type(self.pointer) is str and self.pointer.upper() == 'QUIT':
                pygame.quit()
                quit()
            elif type(self.pointer) is Menu:
                return self.pointer
                
                
        def getLetters(self):
            '''
            returns a dictionary of images with the keys being the letters which point to the image of that letter
            '''
            letters = {}
            for letter in string.ascii_letters:           
                letters[letter.upper()] = pygame.image.load(self.path + letter.upper() + '.png')
            return letters
        def getTextBox(self):
            text = self.text.upper()
            letterCount = 0
            phrase = []
            line = []
            for letter in text:
                if letter is ' ':
                    line.append(' ')
                    letterCount +=1
                    if letterCount > self.lettersPerLine:
                        phrase.append(line)
                        line = []
                        letterCount = 0
                    continue
                line.append(self.letters[letter])            
                letterCount +=1
            phrase.append(line)
            size = (len(max(phrase, key=len))*16,len(phrase)*20)
            surf = pygame.Surface(size)
            x,y = 0,0
            for line in phrase:
                for letter in line:
                    if letter is ' ':
                        x += 16
                        continue
                    surf.blit(letter,(x,y))
                    x += 16
                x = 0
                y += 20

            return surf,size
 
        def draw(self,screen):
            screen.blit(self.img, (self.x-self.size[0]/2,self.y-self.size[1]/2))
            
        
