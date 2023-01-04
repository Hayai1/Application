import pygame
from scripts.input import Input
class MenuInput(Input):
    def __init__(self,menuManager):
        self.menuManager = menuManager
        super().__init__()
    def specificUpdate(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.menuManager.click = True
            

            