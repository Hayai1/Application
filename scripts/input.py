import pygame
import time

class Input:
    def __init__(self):
        self.slowDown = False
    def update(self):
        self.slowDownUpdate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.slowDown = not self.slowDown
            self.specificUpdate(event)
    def slowDownUpdate(self):
        if self.slowDown:
            time.sleep(0.5) 
        