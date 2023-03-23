import pygame
import time
from abc import ABC, abstractmethod

class Input():#the input class
    def __init__(self):#create the input
        self.slowDown = False#slow down the game (used for testing)
    def update(self):#update the input
        self.slowDownUpdate()#slow down the game (used for testing)
        for event in pygame.event.get():#get all the events
            if event.type == pygame.QUIT:#if the user clicks the x in the top right corner
                pygame.quit()#quit pygame
                quit()#quit python
            if event.type == pygame.KEYDOWN:#if a key is pressed
                if event.key == pygame.K_F1:#if the key is f1
                    self.slowDown = not self.slowDown#toggle the slow down var
            self.specificUpdate(event)#update the input
    @abstractmethod#make the function abstract
    def specificUpdate(self,event):pass#specific update to be overriden by the child class
    def slowDownUpdate(self):#slow down the game (used for testing)
        if self.slowDown:#if the slow down var is true
            time.sleep(0.5)#slow down the game by stopping every frame for 0.5 seconds
        