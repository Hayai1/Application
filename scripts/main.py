
import pygame,threading,time
from world import World
from player import Player
from window import Window
from camera import Camera
import enemy
from enemy import *
import AITEST
from AITEST import *
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

window = Window((700,500),"Nea Project",60)
surface = window.createNewSurface((300,200))
world1 = World(50)
player1 = Player(0,0)
enemy1 = Enemy(0, 0)
ai = solveClass()
camera = Camera(player1)

# -------- Main Program Loop -----------
while True:
    window.screen.fill(BLACK)
    #<--------------------------------move through Ai Path-------------------------->
    enemy1.update(ai,NODE_THRESHOLD,world1,player1)
    #<------------------------------------------------------------------------------->
    #<------------------------------solve for path----------------------------------->
    

    #<------------------------------------------------------------------------------->
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.left = True
            if event.key == pygame.K_RIGHT:
                player1.right = True
            if event.key == pygame.K_UP:
                player1.triggerJump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player1.left = False
            if event.key == pygame.K_RIGHT:
                player1.right= False
            if event.key == pygame.K_UP:
                player1.triggerJump = False
                
    camera.update()
    surface.fill(BLACK)
    for room in world1.rooms:
        surface.blit(room.roomImg,(room.x-camera.scroll[0],room.y-camera.scroll[1]))
    
    enemy1.move(world1.rects)
    player1.move(world1.rects)
    
    player1.drawPlayer(surface,camera.scroll)
    enemy1.drawPlayer(surface,camera.scroll)
    window.screen.blit(pygame.transform.scale(surface,window.windowSize),(0,0))
    
    # --- Limit to 60 frames per second
    pygame.display.update()
    window.clock.tick(60)
    
# Close the window and quit.
pygame.quit()
