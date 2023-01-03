import pygame
import time
'''
pygame.time.delay(100)
'''
class Input:
    def __init__(self,player):
        self.player = player
        self.slowDown = False
    def update(self):
        if self.slowDown:
            time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if self.player.takeInputs:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.left = True
                    if event.key == pygame.K_RIGHT:
                        self.player.right = True
                    if event.key == pygame.K_UP:
                        self.player.playerJump()
                    if event.key == pygame.K_1:
                        print("slowed")
                        self.slowDown = True
                    if event.key == pygame.K_2:
                        print("quickend")
                        self.slowDown = False
                    if event.key == pygame.K_3:
                        print("stop")
                    if event.key == pygame.K_4:
                        self.enemy.playerJump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.left = False
                    if event.key == pygame.K_RIGHT:
                        self.player.right= False
                    if event.key == pygame.K_UP:
                        self.player.triggerJump = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.attack = True
            