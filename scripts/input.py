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
            self.specificUpdate(event)
    def slowDownUpdate(self):
        if self.slowDown:
            time.sleep(0.1) 
        