import pygame,sys
from scripts.character import Character
from scripts.animations import Animations
from scripts.sword import Sword
from scripts.playerInput import PlayerInput
class Player(Character):
    def __init__(self,name,x, y,hp, width, height,collisionRects,hpBarImg=None):#init the player
        super().__init__(x, y, width, height,collisionRects)#init the character class
        self.name = name#name of the player
        self.weapons = {'sword' : Sword(x,y)}#the weapons the player has
        self.takeInputs = True#does the player take inputs
        self.attacking = False#is the player attacking
        self.dash = False#is the player dashing
        self.slide = False#is the player sliding
        self.dead = False#is the player dead
        self.input = PlayerInput(self)#the player's input
        self.slideVel = None#the velocity of the player when sliding
        self.slideAcc = None#the acceleration of the player when sliding
        self.imunityFrames = 0#the amount of frames the player is immune to damage
        self.dashAcceleration = 0.5#the acceleration of the player when dashing
        self.attackCombo = 'firstAttack'#the attack combo the player is on
        self.hpBar = self.getHpBar(hp,hpBarImg)#the hp bar of the player
        self.animations = self.getAnimations('assets/playerAnimations',run=[4,4,4,4,4],#the animations of the player
                                             idle=[1],firstAttack=[4,4,4,4,4,4],secondAttack=[5,5,4,4],
                                             thirdAttack=[5,10,4],dash=[4,5,5,5,5,5])
    
    @property
    def isInIngameMenu(self):#is the player in the in game menu
        return self.input.runInGameMenu
    
    def drawPlayerHpBar(self,gameSurface):#draw the player's hp bar
        pygame.draw.rect(gameSurface,(172,50,50),(9,9+170,self.hpBarWidth-10,self.hpBar['height']-10))#draw the red hp bar
        gameSurface.blit(self.hpBar['img'],(4,4+170))#draw the hp bar image
    

    def attack(self):#attack function
        if self.attackCombo =='firstAttack':#if the attack combo is the first attack
            self.triggerAttack1()#call the triggerAttack1 function
        elif self.attackCombo == 'secondAttack':#if the attack combo is the second attack
            self.triggerAttack2()#call the triggerAttack2 function
        elif self.attackCombo == 'thirdAttack':#if the attack combo is the third attack
            self.triggerAttack3()#call the triggerAttack3 function
        
    def triggerAttack1(self):#trigger the first attack
        self.animations.changeState('firstAttack')#change the animation state to firstAttack
        currentImg = self.animations.getCurrentImg#get the current image of the animation
        if currentImg == 'firstAttack2':#if the current image is the second image of the first attack
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip,'down')#create a new bezeir arc
            self.startSlide()#start the slide
        elif currentImg == 'firstAttack5':#if the current image is the fifth image of the first attack
            self.attacking = False#stop attacking
            self.attackCombo = 'secondAttack'#change the attack combo to the second attack

    def triggerAttack2(self):#trigger the second attack
        self.animations.changeState('secondAttack')#change the animation state to secondAttack
        currentImg = self.animations.getCurrentImg#get the current image of the animation
        if currentImg == 'secondAttack2':#if the current image is the second image of the second attack
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip,'up')#create a new bezeir arc
            self.startSlide()#start the slide
        elif currentImg == 'secondAttack3':#if the current image is the third image of the second attack
            self.attacking = False#stop attacking
            self.attackCombo = 'thirdAttack'#change the attack combo to the third attack
    def triggerAttack3(self):#trigger the third attack
        self.animations.changeState('thirdAttack')#change the animation state to thirdAttack
        currentImg = self.animations.getCurrentImg#get the current image of the animation
        if currentImg == 'thirdAttack0':#if the current image is the first image of the third attack
            self.startSlide()#start the slide
            self.weapons["sword"].arc = self.weapons["sword"].newBezeirArc(self.x,self.y,self.flip,'down')#create a new bezeir arc
        elif currentImg == 'thirdAttack2':#if the current image is the third image of the third attack
            self.attacking = False#stop attacking
            self.attackCombo = 'firstAttack'#change the attack combo to the first attack
    def triggerDash(self):#trigger the dash
        self.attacking = False#stop attacking
        if self.flip: #if the player is flipped
            self.velocity[0] = -(6 / self.dashAcceleration)#set the velocity to the dash acceleration
            self.dashAcceleration += 0.5#increase the dash acceleration
        else: #if the player is not flipped
            self.velocity[0] = (6 / self.dashAcceleration)#set the velocity to the dash acceleration
            self.dashAcceleration += 0.5#increase the dash acceleration
        self.animations.changeState('dash')#change the animation state to dash
        currentImg = self.animations.getCurrentImg#get the current image of the animation
        if currentImg == 'dash5':#if the current image is the fifth image of the dash
            self.dash = False#stop dashing
            self.dashAcceleration = 0.5#reset the dash acceleration
    
    def changeAnimationState(self,movement):#change the animation state
        if movement[0] == 0:self.animations.changeState('idle')#if the player is not moving change the animation state to idle
        if movement[0] > 0:self.animations.changeState('run')#if the player is moving right change the animation state to run
        if movement[0] < 0:self.animations.changeState('run')#if the player is moving left change the animation state to run

    def kill(self):#kill the player
        self.hpBar['hp'] = 100#reset the hp
        self.dead = True#set the player to dead
    
    def startSlide(self):#start the slide
        self.slideVel = 3#set the slide velocity
        self.slideAcc = -1#set the slide acceleration
        self.slide = True#set the slide to true
    
    def slideUpdate(self):#update the slide
        if self.slide:#if the player is sliding
            self.slideVel += self.slideAcc#increase the slide velocity
            if self.flip: self.x -=self.slideVel#move the player left
            else: self.x += self.slideVel#move the player right
            if self.slideVel <= 0:#if the slide velocity is less than or equal to 0
                self.slide = False#stop sliding
                self.slideVel = None#reset the slide velocity
                self.slideAcc = None#reset the slide acceleration
    
    def update(self,gameSurface,scroll, enemies):#update the player
        self.updateCharacter()#update the character
        self.input.update()#update the input
        if not self.attacking:#if the player is not attacking
            movement = self.move(self.collisionRects)#move the player
        if self.dash: self.triggerDash()#if the player is dashing call the triggerDash function
        elif self.attacking: #if the player is attacking
            self.attack()#call the attack function
        else: self.changeAnimationState(movement)#change the animation state

        self.slideUpdate()#update the slide
        add = 0#set the add variable to 0
        if self.animations.getCurrentImg[:-1] == 'thirdAttack':#if the current image is the third attack
            if self.flip: add = -13#set the add variable to -13
            else: add = 13#set the add variable to 13
        self.weapons['sword'].update(self.x+add,self.y,gameSurface,scroll,enemies)#update the sword add to the x position of the player so that it's in the correct postion depending on the animation
        
        self.draw(gameSurface,scroll,self.animations.getImg())#draw the player
        self.drawPlayerHpBar(gameSurface)#draw the player hp bar
        




        