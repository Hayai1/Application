from scripts.input import Input
import pygame
class PlayerInput(Input):
    def __init__(self,player):
        self.player = player
        self.enemy = None
        super().__init__()
    def specificUpdate(self,event):
        if self.player.takeInputs:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.left = True
                if event.key == pygame.K_RIGHT:
                    self.player.right = True
                if event.key == pygame.K_UP:
                    self.player.playerJump()
                if event.key == pygame.K_0:
                    self.enemy.attack()
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
