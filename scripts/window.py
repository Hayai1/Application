#import pygame
import pygame

class Window:#window class
    '''
    #constructor function for the window class takes 2 arguments: 
    windowSize = (width of the window,height of the window),
    windowTitle= the text to be displayed at the top of the window),
    fps = the frames per second the window will run at
    '''
    def __init__(self,windowSize,windowTitle="placeHolder",fps=60,):
        self.windowSize = windowSize#set the window size
        self.fps = fps#set the fps
        self.running = True#set the running variable to true
        self.screen = pygame.display.set_mode(windowSize,pygame.RESIZABLE)#create a new window (pygame function)
        self.clock = pygame.time.Clock()#create a new clock (pygame function)
        pygame.display.set_caption(windowTitle)#set the window title (pygame function)
        self.GameSurface = pygame.Surface((300,200))#create a new surface to draw on which will be scaled to the window size

    def update(self):#update function for Window class
        self.screen.fill((0, 0, 0))#fill the screen with black to empty it
        self.screen.blit(pygame.transform.scale(self.GameSurface,[self.screen.get_width(),self.screen.get_height()]),(0,0))#scale up the game surface to the window size and draw it to the screen at position 0,0 
        pygame.display.flip()#update the screen (pygame function)
        self.GameSurface.fill((0, 0, 0))#fill the game surface with black to empty it
        self.clock.tick(self.fps)#tick the clock to the fps (pygame function)
        
        
        