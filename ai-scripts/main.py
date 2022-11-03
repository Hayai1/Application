#Michael Schrandt   00616486
#12/6/2011
#driver file. Main Loop is defined here.


from turtle import Turtle
import pygame


import Map
from Map import *

import Player
from Player import *

import AITEST
from AITEST import *

import threading

pygame.init()
quitGame = False
#Global constants
WIDTH = 640
HEIGHT = 480
#Window stuff
while (not quitGame):
    #Game stuff
    path = None
    command = input('Input Command: ')
    if (command == 'quit'):
        break
    command = command.split(' ')
    if (command[0] == 'solve'):
        view = pygame.Rect(0, 0, WIDTH, HEIGHT)
        s, start, end = readMap('ai-scripts/' +command[1])

        start[0] = (int(start[0])*32)+PLAYER_W
        start[1] = (int(start[1])*32)+PLAYER_W/2
        end[0] = (int(end[0])*32)+32
        end[1] = (int(end[1])*32)+16
        enemy = Player(start[1], start[0],0)
        player = Player(end[1], end[0], 0)
        enemyXVelocity = 0
        playerXVelocity = 0
        solveObj = solveClass()
        solved = True
        solve = threading.Thread(target=solveObj.solve, args=(s, (player.location.y, player.location.x), (end[0], end[1]),))
    else:
        continue
    screenSize = [WIDTH, HEIGHT]
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Platforming AI")
    done = False
    clock = pygame.time.Clock()
    currentStep = 0
    while not done:
        #<--------------------------------move through Ai Path-------------------------->
        if (not solve.is_alive()):
            if (solveObj.path is not None and currentStep/NODE_THRESHOLD < len(solveObj.path)):
                if (solveObj.path[int(currentStep/NODE_THRESHOLD)].y < enemy.location.bottom):
                    enemy.jump()
                elif (enemy.yVelocity < 0):
                    enemy.yVelocity = 0
                if (solveObj.path[int(currentStep/NODE_THRESHOLD)].x > enemy.location.center[0]):
                    enemyXVelocity = MAX_SPEED
                elif (solveObj.path[int(currentStep/NODE_THRESHOLD)].x < enemy.location.center[0]):
                    enemyXVelocity = -1*MAX_SPEED
                else:
                    enemyXVelocity = 0
                currentStep += 1
            else:
                enemyXVelocity = 0
                nextSolve = True
        #<------------------------------------------------------------------------------->
        #<------------------------------solve for path----------------------------------->
        if nextSolve and player.inAggroRange(enemy) and not player.inAttackRange(enemy):
            solve = threading.Thread(target=solveObj.solve, 
                                    args=(s, 
                                          (enemy.location.y, enemy.location.x), 
                                          (player.location.y, player.location.x)
                                        ,))
            solve.start()
            currentStep = 0
            nextSolve = False
        #<------------------------------------------------------------------------------->

        #<----------------------------------handle events-------------------------------->
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXVelocity = -MAX_SPEED
                if event.key == pygame.K_RIGHT:
                    playerXVelocity = MAX_SPEED
                if event.key == pygame.K_UP:
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerXVelocity = 0
                if event.key == pygame.K_RIGHT:
                    playerXVelocity = 0
        #<------------------------------------------------------------------------------->


        #Move the player
        enemy.move(enemyXVelocity, s)
        player.move(playerXVelocity, s)
        #Adjust the camera
        view.center = player.location.center
        if (view.left < 0):
            view.left = 0
        elif (view.right > (len(s[0]) * 32)):
            view.right = len(s[0]) * 32
        if (view.top < 0):
            view.top = 0
        elif (view.bottom > (len(s)*32)):
            view.bottom = len(s)*32
        #<------------------------------------drawing stuff-------------------------------->
        
        screen.fill((0,0,0))
        drawMap(screen, s, view, [end[0]-32, end[1]-16])
        if (solveObj.path is not None):
            drawPath(screen, solveObj.path, view)
        player.draw(screen, view,[0,0,200])
        if player.inAggroRange(enemy) and not player.inAttackRange(enemy):
            enemy.draw(screen, view, [0,200,0])
        elif player.inAttackRange(enemy):
            enemy.draw(screen,view,[200,0,0])
        else:
            enemy.draw(screen,view,(255,255,255))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()
pygame.quit()



