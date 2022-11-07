
import pygame,sys

mainClock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')

screen = pygame.display.set_mode((500,500),0,32)
Surface = pygame.Surface((300,300))

def diamond():
    p1 = [0,0]
    p2 = [500,0]
    points = [p1,p2]
    return points
while True:
    screen.fill((0,0,0))
    Surface.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pass
            
    diamondPoints = diamond()
    pygame.draw.polygon(Surface,(255,0,0),diamondPoints,0)

 
    mx,my = pygame.mouse.get_pos()

    screen.blit(Surface,(mx-50,my-50))

    pygame.display.update()
    mainClock.tick(60)