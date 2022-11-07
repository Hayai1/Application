
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

 


PLAYER_W = 32
start = [0,0]
end = [0,0]
s = world1.WorldIn01
start[0] = (int(start[0])*32)+PLAYER_W
start[1] = (int(start[1])*32)+PLAYER_W/2
end[0] = (int(end[0])*32)+32
end[1] = (int(end[1])*32)+16
rects = []
for room in world1.rooms:
    for rect in room.rects:
        rects.append(rect)
player1 = Player(0,0,rects)
enemy1 = Player(start[1], start[0],rects)
enemyXVelocity = 0
playerXVelocity = 0
currentStep = 0


solveObj = solveClass()
solved = True
solve = threading.Thread(target=solveObj.solve, args=(s, (player1.rect.y, player1.rect.x), (end[0], end[1]),rects,))


camera = Camera(player1)
# -------- Main Program Loop -----------
while True:
    enemy1.triggerJump = False
    window.screen.fill(BLACK)
    #<--------------------------------move through Ai Path-------------------------->
    if (not solve.is_alive()):
        if (solveObj.path is not None and currentStep/NODE_THRESHOLD < len(solveObj.path)):
            if (solveObj.path[int(currentStep/NODE_THRESHOLD)].y < enemy1.rect.bottom):
                enemy1.triggerJump = True
            elif (enemy1.velocity[1] < 0):
                enemy1.velocity[1] = 0
            if (solveObj.path[int(currentStep/NODE_THRESHOLD)].x > enemy1.rect.center[0]):
                enemy1.velocity[0] = MAX_SPEED
            elif (solveObj.path[int(currentStep/NODE_THRESHOLD)].x < enemy1.rect.center[0]):
                enemy1.velocity[0] = -1*MAX_SPEED
            else:
                enemy1.velocity[0] = 0
            currentStep += 1
        else:
            enemy1.velocity[0] = 0
            nextSolve = True
    #<------------------------------------------------------------------------------->
    #<------------------------------solve for path----------------------------------->
    
    if nextSolve and player1.inAggroRange(enemy1) and not player1.inAttackRange(enemy1):
        solve = threading.Thread(target=solveObj.solve, 
                                args=(s, 
                                        (enemy1.rect.y, enemy1.rect.x), 
                                        (player1.rect.y, player1.rect.x)
                                    ,rects,))
        solve.start()
        currentStep = 0
        nextSolve = False
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
    
    enemy1.move()
    player1.move()
    
    player1.drawPlayer(surface,camera.scroll)
    enemy1.drawPlayer(surface,camera.scroll)
    window.screen.blit(pygame.transform.scale(surface,window.windowSize),(0,0))
    
    # --- Limit to 60 frames per second
    pygame.display.update()
    window.clock.tick(60)
    
# Close the window and quit.
pygame.quit()
