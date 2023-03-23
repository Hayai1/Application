import pygame
from scripts.input import Input

                
class MenuInput(Input):#input for the menu
    def __init__(self):#create the input
        self.input =[None, None]#the key pressed [the key pressed, the mouse button pressed]
        super().__init__()
    def specificUpdate(self,event):#override the specific update function
        
        if event.type == pygame.MOUSEBUTTONDOWN:#if the mouse is pressed
            input = self.input#get the input 
            input[1] = event.button#set the new input vars mouse index to the button pressed 
            self.input = input#set the input to the input var
                
        elif event.type == pygame.KEYDOWN:#if a key is pressed
            input = self.input#get the input
            if event.key == 8:#if the key is backspace
                input[0] = 'backspace'#set the input var to backspace
            else:#if the key is not backspace
                try: #try to set the input var to the key pressed as a char
                    input[0] = chr(event.key)#set the input var to the key pressed as a char
                except:#if the key is not a char e.g. symbol (!?$...) or number (1234...)
                    input = [None, False]#set the input var to none
            self.input = input#set the input to the input var
            
    @property
    def input(self):#get the input
        input = self._input#set the input to the input var
        self._input = [None,None]#reset the input so that it is not held down
        return input#return the input
    @input.setter#set the input
    def input(self,value):#set the input
        self._input = value#set the input var to the value
