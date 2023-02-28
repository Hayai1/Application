import pygame
from scripts.input import Input

                
class MenuInput(Input):
    def __init__(self):
        self.key =[None, False]
        super().__init__()
    def specificUpdate(self,event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = self.key
            key[1] = event.button
            self.key = key
                
        elif event.type == pygame.KEYDOWN:
            key = self.key
            if event.key == 8:
                key[0] = 'backspace'
            else:
                try: 
                    key[0] = chr(event.key)
                except:
                    key = [None, False]
            self.key = key
            
    @property
    def key(self):
        key = self._key
        self._key = [None,None]
        return key
    @key.setter
    def key(self,value):
        self._key = value
