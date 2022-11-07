import pygame

class Input:
    def update(self,player1):
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