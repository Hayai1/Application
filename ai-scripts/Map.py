#Michael Schrandt   00616486
#12/6/2011
#Maps are read and drawn
import pygame

#Tile attributes
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (200, 75, 0)
ORANGE = (255, 75, 0)
GREEN= (0, 175, 0)
BLUE = (0, 175, 250)
PURPLE = (175, 0, 175)
YELLOW = (220, 220, 0)
colors = {0:BLACK, 1:WHITE, 2:RED, 3:GREEN, 4:BLUE}
collidable = (1,2,3)

#store the map in a 2-D array of integers
def readMap(inputFile):
    try:
        f = open(inputFile)
    except:
        return None, None, None
    #if (not f):
    #    return None, None, None
    start = f.readline().split(',')
    end = f.readline().split(',')
    lines = f.readlines()
    f.close()
    
    for i in range(0, len(lines)):
        lines[i] = lines[i].split()
        for j in range(len(lines[i])):
            lines[i][j]= int(lines[i][j])

    return lines, start, end

def printMap(myMap):
    for i in range(len(myMap)):
        for j in range(len(myMap[i])):
            print (myMap[i][j],)

#draw a 2-D array to the screen
def drawMap(screen, map, viewRect, end):

    #only draw visible parts (plus one extra tile around the border)
    starti = int(viewRect.top/32)
    endi = int((viewRect.top+viewRect.height)/32)+1
    startj = int(viewRect.left/32)
    endj = int((viewRect.left+viewRect.width)/32)+1

    #make sure that the "border" we added even exists
    if (endi > len(map)):
        endi = len(map)
    if (endj > len(map[0])):
        endj = len(map[0])

    #iterate through the array, drawing a rectangle for each tile as its
        #appropriate color
    for i in range(starti,endi ):
        for j in range(startj,endj ):
            pygame.draw.rect(screen, colors.get(map[i][j]),
                             [j*32-viewRect.left, i*32-viewRect.top, 31, 31], 0)
    pygame.draw.rect(screen, YELLOW, [end[1] - viewRect.left, end[0]-viewRect.top, 31, 31], 0)

def drawPath(screen, path, view):
    for i in range(len(path)-1):
        pygame.draw.line(screen, ORANGE, (path[i].x - view.left,path[i].y-view.top), (path[i+1].x-view.left,path[i+1].y-view.top), 2)
