import pygame

class Input:
    def __init__(self,player):
        self.player = player
    def update(self):
        if self.player.takeInputs:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.left = True
                    if event.key == pygame.K_RIGHT:
                        self.player.right = True
                    if event.key == pygame.K_UP:
                        self.player.triggerJump = True
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
            