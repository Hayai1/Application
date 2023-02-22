from scripts.input import Input
import pygame
class PlayerInput(Input):
    def __init__(self,player):
        self.player = player
        super().__init__()
    def specificUpdate(self,event):
        if self.player.takeInputs:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.left = True
                if event.key == pygame.K_d:
                    self.player.right = True
                if event.key == pygame.K_SPACE:
                    self.player.playerJump()
                if event.key == pygame.K_LSHIFT:
                    self.player.dash = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.left = False
                if event.key == pygame.K_d:
                    self.player.right= False
                if event.key == pygame.K_UP:
                    self.player.triggerJump = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.player.weapons["sword"].arcDone:
                        self.player.attacking = True
                    
