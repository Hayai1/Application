import pygame
class Window:
    def __init__(self,WINDOW_SIZE= (1920,1080), windowTitle = "My Game", fps = 60):
        self.WINDOW_SIZE = WINDOW_SIZE
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(windowTitle)
        self.clock = pygame.time.Clock()
        self.fps = 60
    def update(self,surface):
        self.screen.blit(pygame.transform.scale(surface,self.WINDOW_SIZE),(0,0))
    
    # --- Limit to 60 frames per second
        pygame.display.update()
        self.clock.tick(60)