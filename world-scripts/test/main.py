'''
create a pygame template
'''

import pygame

pygame.init()

# Global constants

WIDTH = 640

HEIGHT = 480

# Window stuff

screenSize = [WIDTH, HEIGHT]

screen = pygame.display.set_mode(screenSize)

pygame.display.set_caption("Platforming AI")

done = False

clock = pygame.time.Clock()
def loadMap(path):
    '''
    Load a map from a file
    '''
    map = []
    with open(path, 'r') as f:
        for line in f:
            map.append(line)
    return map
def drawMap(map):
    pass

path = 'world-scripts/test/map.txt'
loadMap(path)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            done = True
    
    # Game stuff
    # Update screen

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

