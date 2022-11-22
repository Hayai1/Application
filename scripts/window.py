import pygame

class Window:
    def __init__(self,windowSize,windowTitle="placeHolder",fps=60,):
        self.windowSize = windowSize
        self.fps = fps
        self.running = True
        self.playtime = 0.0
        self.screen = pygame.display.set_mode(windowSize)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('mono', 20, bold=True)
        pygame.display.set_caption(windowTitle)
    def createNewSurface(self,size):
        return pygame.Surface(size)
    def update(self,surface):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(surface,self.windowSize),(0,0))
        self.screen.blit(self.font.render("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(self.clock.get_fps(), " "*5, self.playtime), True, (255, 255, 255)), (5, 5))
        pygame.display.flip()
        self.playtime += self.clock.tick(self.fps) / 1000.0
        
        
        