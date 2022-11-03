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
    rects = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '1':
                rects.append(pygame.Rect(x * 32, y * 32, 32, 32))
    return rects 

path = 'world-scripts/test/map.txt'
map = loadMap(path)
print(map)
rectMap = drawMap(map)
while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            done = True
    
    # Game stuff
    # Update screen
    for i in rectMap:
        pygame.draw.rect(screen, (255, 255, 255), i)
    pygame.display.update()
    
    clock.tick(60)

pygame.quit()

