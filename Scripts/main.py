
import pygame,threading,time
from world import World
from player import Player
from inputs import Inputs
from camera import Camera
from window import Window
import enemy
from enemy import *
import AITEST
from AITEST import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
window = Window()
surface = pygame.Surface((300,200))
world1 = World(50)
input = Inputs()

s = world1.WorldIn01

rects = world1.getRects()
enemy1 = Enemy(rects,32)
player1 = Player(0,0,rects)
camera = Camera(player1)
done = False



enemyXVelocity = 0
playerXVelocity = 0
currentStep = 0
solveObj = solveClass()
solved = True
solve = threading.Thread(target=solveObj.solve, args=(s, (player1.rect.y, player1.rect.x), (enemy1.end[0], enemy1.end[1]),rects,))



# -------- Main Program Loop -----------
while not done:
    window.screen.fill(BLACK)
    surface.fill(BLACK)
    input.update(player1)
    camera.update()
    world1.update(surface,camera.scroll)
    enemy1.update(solveObj, solve, NODE_THRESHOLD,player1,s,rects,surface,camera.scroll)
    player1.update(surface,camera.scroll)
    window.update(surface)
    
    # --- Limit to 60 frames per second
    
# Close the window and quit.
pygame.quit()
