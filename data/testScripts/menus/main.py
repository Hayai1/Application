import pygame
from menu import Menu
from cursor import Cursor
class Game:
    def __init__(self):
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        pygame.init()
        

        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)
        
        pygame.display.set_caption("My Game")
        self.menuDone = False
        self.done = False
        self.clock = pygame.time.Clock()

        self.cursor = Cursor()
        
        #create the menus
        self.createCharacter = Menu('character creation')
        self.openingScreen = Menu('opening screen')
        self.characterSelection = Menu('character selection')
        #openingScene
        gameTitle = self.openingScreen.createTextBox('assets/letters/','GameName',"Game name",350,100,30)
        exitButton = self.openingScreen.createTextBox('assets/letters/','Exit',"Exit",350,400,30,'quit')
        startButton = self.openingScreen.createButton('assets/buttons/play.png','startButton',350,200,self.characterSelection)
        #characterSelection
        createNewCharacterButton = self.characterSelection.createTextBox('assets/letters/','newGameCreation','create new character',350,100,30,self.createCharacter)
        characterListName = self.characterSelection.createTextBox('assets/letters/','characterListName','character list',350,200,30)
        backButton = self.characterSelection.createTextBox('assets/letters/','back','back',350,400,30,self.openingScreen)
        #characterCreation
        characterNameIntro = self.createCharacter.createTextBox('assets/letters/','characterNameIntro','enter character name',350,100,30)
        characterNameInput = self.createCharacter.createTypeBar(350,200)
        
        
        #START THE MENU
        self.startMenu()
        #self.runGame()
    def startMenu(self):
        currentMenu = self.openingScreen
        while not self.menuDone:
            self.screen.fill(self.BLACK)
            currentMenu = currentMenu.update(self.screen,self.cursor)
            self.cursor.update()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.menuDone=True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.click = True
                if currentMenu.typing:
                    if event.type == pygame.KEYDOWN:
                        print(event.key)
            pygame.display.flip()
            
    def runGame(self):
        while not self.done:
            self.screen.fill(self.BLACK)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.done=True
                

            self.clock.tick(60)
            
        pygame.quit()
 
# -------- Main Program Loop -----------
if __name__ == "__main__":
    game = Game()