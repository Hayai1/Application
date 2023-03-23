import pygame
from scripts.animations import Animations
class Character:
    def __init__(self,x,y,width,height,collisionRects):#create the character
        self.left = False#is the character moving left
        self.right = False# is the character moving right
        self.airTimer = 0#how long the character has been in the air
        self.flip = False#is the character flipped
        self.velocity = [0,0]#the character's velocity
        self.acceleration = [0,0]#the character's acceleration
        self.rect = pygame.Rect(x,y,width,height)#the character's rect
        self.x = x #the character's x position
        self.y = y#the character's y position
        self.maxHp = 100#the character's max hp
        self.collisionRects = collisionRects#the character's collision rects
        self.collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}#the character's collision types
    @property
    def width(self):
        return self.rect.width
    @property
    def height(self):
        return self.rect.height
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @x.setter
    def x(self,value):
        self._x = value
        self.rect.x = value 
    @y.setter
    def y(self,value):
        self._y = value
        self.rect.y = value
    def getAnimations(self,animationRootDir,**kwargs):#get the character's animations
        animations = Animations(animationRootDir)#create a new animations object
        for key,value in kwargs.items():#for each key value pair in kwargs
            animations.getAnimation(key,value)#get the animation
        return animations#return the animations object
    
    def takeDamage(self,damage):#take damage
        if self.imunityFrames <= 0:#if the character is not immune 
            self.imunityFrames = 20#set the imunity frames to 20 so that the character can't take damage for each 20 frames
            self.hpBar['hp'] -=damage#take damage
            if self.hpBar['hp'] <= 0:#if the character's hp is less than or equal to 0
                self.kill()#kill the character
            

    #virtual
    def draw(self,surface,scroll,img):#draw the character
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.x-9-scroll[0],self.y-9-scroll[1]))#draw the character

    def getCollisions(self,tiles):#get the collisions
        collisions = []#create a list of collisions
        for tile in tiles:#for each tile in the tiles list
            if self.rect.colliderect(tile):#if the character's rect collides with the tile
                collisions.append(tile)#add the tile to the collisions list
        return collisions#return the collisions list
    
    def getHpBar(self,hp,path):#get the hp bar
        hpBar = {}#create a new hp bar 
        img = pygame.image.load(path)#load the image
        img.set_colorkey((0,0,0))#set the color key (to make the image transparent)
        hpBar['img'] = img#set the image
        hpBar['height'] = img.get_height()#set the height
        hpBar['hp'] = hp#set the hp (int)
        hpBar['hpPercentage'] = 100#set the hp percentage
        return hpBar#return the hp bar
    @property
    def hpBarWidth(self):#get the hp bar width
        width = self.hpBar['img'].get_width() #get the width of the hp bar image
        percentage = (self.hpBar['hpPercentage'] / 100)#get the percentage of the hp bar
        return width * percentage#return the width of the hp bar
    
    def updateVelocity(self):
        self.velocity[0] += self.acceleration[0]#update the velocity x component
        self.velocity[1] += self.acceleration[1]#update the velocity y component
        if self.left:#if the character is moving left
            self.velocity[0] -= 2#decrease the velocity x component by 2
        if self.right:#if the character is moving right
            self.velocity[0] += 2#increase the velocity x component by 2
            
    def jump(self):#jump
        if self.airTimer < 6:#if the character is in the air for less than 6 frames
            self.acceleration[1] = -6#set the acceleration y component to -6

    def updateCharacter(self):#update the character
        self.imunityFrames -= 1#decrease the imunity frames by 1
        self.hpBar["hpPercentage"] = (self.hpBar["hp"]/self.maxHp)*100#update the hp bar percentage
        self.x = self.rect.x #update the x position
        self.y = self.rect.y#update the y position

    def move(self,rectsToCollide):#move the character
        self.collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}#reset the collision types
        if self.acceleration[1] < 3:#if the acceleration y component is less than 3
            self.acceleration[1] += 0.2#increase the acceleration y component by 0.2
        self.updateVelocity()#update the velocity
        self.rect.x += self.velocity[0]#move the characters rect x component by the velocity x component to check for collisions in the x direction
        collisions = self.getCollisions(rectsToCollide)#get the collisions 
        for tile in collisions:#for each tile in the collisions list due to only moving in the x direction all colisions will be to the side of the character rect
            if self.velocity[0] > 0:#if the velocity x component is greater than 0 (moving right)
                self.rect.right = tile.left#set the rect right to the tile left (so that the character rect is touching the tile)
                self.collisionTypes['right'] = True#set the right collision type to true
            elif self.velocity[0] < 0:#if the velocity x component is less than 0 (moving left)
                self.rect.left = tile.right#set the rect left to the tile right (so that the character rect is touching the tile)
                self.collisionTypes['left'] = True#set the left collision type to true
        self.rect.y += self.velocity[1]#move the characters rect y component by the velocity y component to check for collisions in the y direction
        collisions = self.getCollisions(rectsToCollide)#get the collisions
        for tile in collisions:#for each tile in the collisions list due to only moving in the y direction all colisions will be to the top or bottom of the character rect
            if self.velocity[1] > 0:#if the velocity y component is greater than 0 (moving down)
                self.rect.bottom = tile.top#set the rect bottom to the tile top (so that the character rect is touching the tile)
                self.collisionTypes['bottom'] = True#set the bottom collision type to true
            elif self.velocity[1] < 0:#if the velocity y component is less than 0 (moving up)
                self.rect.top = tile.bottom#set the rect top to the tile bottom (so that the character rect is touching the tile)
                self.collisionTypes['top'] = True  #set the top collision type to true
        if self.collisionTypes['bottom']:#if the character is on the ground
            self.airTimer = 0#set the air timer to 0
            self.acceleration = [0,0]#set the acceleration to 0 as the character is on the ground
        elif self.collisionTypes['top']:#if the character is on the top of a tile
            self.acceleration = [0,0]#set the acceleration to 0 so the character falls when they hit there head on a tile above them
        else:
            self.airTimer += 1#increase the air timer by 1 since in the air
        movement = self.velocity#set the movement to the velocity
        if movement[0] > 0:#if the movement x component is greater than 0 (moving right)
            self.flip = False#set the flip to false
        if movement[0] < 0:#if the movement x component is less than 0 (moving left)
            self.flip = True#set the flip to true
        self.velocity = [0,0]#set the velocity to 0
        self.acceleration[0] = 0#set the acceleration x component to 0
        return movement#return the movement