import pygame
from scripts.animations import Animations
class Character:
    def __init__(self,x,y,width,height,collisionRects):
        self.left = False
        self.right = False
        self.triggerJump = False
        self.airTimer = 0
        self.flip = False
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.rect = pygame.Rect(x,y,width,height)
        self.x = x 
        self.y = y
        self.maxHp = 100
        self.collisionRects = collisionRects
        self.collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
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
    def getAnimations(self,animationRootDir,**kwargs):
        animations = Animations(animationRootDir)
        for key,value in kwargs.items():
            animations.getAnimation(key,value)
        return animations
    
    def takeDamage(self,damage):
        if self.imunityFrames <= 0:
            self.imunityFrames = 10
            self.hpBar['hp'] -=damage
            if self.hpBar['hp'] <= 0:
                self.kill()
        else:
            self.imunityFrames -= 1


    def draw(self,surface,scroll,img):
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.x-9-scroll[0],self.y-9-scroll[1]))

    def getCollisions(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def getHpBar(self,hp,path):
        hpBar = {} 
        img = pygame.image.load(path)
        img.set_colorkey((0,0,0))
        hpBar['img'] = img
        hpBar['height'] = img.get_height()
        hpBar['hp'] = hp
        hpBar['hpPercentage'] = 100
        return hpBar
    @property
    def hpBarWidth(self):
        width = self.hpBar['img'].get_width() 
        percentage = (self.hpBar['hpPercentage'] / 100)
        return width * percentage
    
    def updateVelocity(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        if self.left:
            self.velocity[0] -= 2
        if self.right:
            self.velocity[0] += 2
            
    def playerJump(self):
        if self.airTimer < 6:
            self.acceleration[1] = -6

    def updateCharacter(self):
        self.x = self.rect.x 
        self.y = self.rect.y

    def move(self,rectsToCollide):
        self.collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
        if self.acceleration[1] < 3:
            self.acceleration[1] += 0.2
        self.updateVelocity()
        self.rect.x += self.velocity[0]
        collisions = self.getCollisions(rectsToCollide)
        for tile in collisions:
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                self.collisionTypes['right'] = True
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                self.collisionTypes['left'] = True
        self.rect.y += self.velocity[1]
        collisions = self.getCollisions(rectsToCollide)
        for tile in collisions:
            if self.velocity[1] > 0:
                self.rect.bottom = tile.top
                self.collisionTypes['bottom'] = True
            elif self.velocity[1] < 0:
                self.rect.top = tile.bottom
                self.collisionTypes['top'] = True  
        if self.collisionTypes['bottom']:
            self.airTimer = 0
            self.acceleration = [0,0]
        elif self.collisionTypes['top']:
            self.acceleration = [0,0]
        else:
            self.airTimer += 1
        movement = self.velocity
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        self.velocity = [0,0]
        self.acceleration[0] = 0
        return movement