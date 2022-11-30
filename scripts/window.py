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
        self.surface = pygame.Surface((300,200))

    def update(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.surface,self.windowSize),(0,0))
        self.screen.blit(self.font.render("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(self.clock.get_fps(), " "*5, self.playtime), True, (255, 255, 255)), (5, 5))
        pygame.display.flip()
        self.surface.fill((0, 0, 0))
        self.playtime += self.clock.tick(self.fps) / 1000.0
        
        
        