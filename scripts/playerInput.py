from scripts.input import Input
import pygame

class PlayerInput(Input):
    def __init__(self,player):#player is the player object
        self.player = player#the player object
        self.runInGameMenu = False#is the ingame menu running
        super().__init__()#call the super class's init function
    def specificUpdate(self,event):#this function is called in the update function of the input class
        if self.player.takeInputs:#if the player can take inputs
            if event.type == pygame.KEYDOWN:#if a key is pressed
                if event.key == pygame.K_a:#if the key is a
                    self.player.left = True#set the player's left variable to true
                if event.key == pygame.K_d:#if the key is d
                    self.player.right = True#set the player's right variable to true
                if event.key == pygame.K_SPACE:#if the key is space
                    self.player.jump()#call the player's jump function
                if event.key == pygame.K_LSHIFT:#if the key is left shift
                    self.player.dash = True#set the player's dash variable to true
                if event.key == pygame.K_ESCAPE:#if the key is escape
                    self.runInGameMenu = True#set the runInGameMenu variable to true
            if event.type == pygame.KEYUP:#if a key is released
                if event.key == pygame.K_a:#if the key is a
                    self.player.left = False#set the player's left variable to false
                if event.key == pygame.K_d:#if the key is d
                    self.player.right= False#set the player's right variable to false
                
            if event.type == pygame.MOUSEBUTTONDOWN:#if the mouse is clicked
                if event.button == 1:#if the left mouse button is clicked
                    if self.player.weapons["sword"].arcDone:#if the sword's arc is done
                        self.player.attacking = True#set the player's attacking variable to true
                    
