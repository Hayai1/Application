import pygame

class Input:
    def update(self,player):
        if player.takeInputs:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.left = True
                    if event.key == pygame.K_RIGHT:
                        player.right = True
                    if event.key == pygame.K_UP:
                        player.triggerJump = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.left = False
                    if event.key == pygame.K_RIGHT:
                        player.right= False
                    if event.key == pygame.K_UP:
                        player.triggerJump = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        player.attack = True
                        #player.weapons['sword'].swing()
            