import pygame
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
        self.collisionRects = collisionRects
        self.animations = self.getAnimations()
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
    def draw(self,surface,scroll,img):
        #pygame.draw.rect(surface,(255,0,0),self.rect)
        surface.blit(pygame.transform.flip(img,self.flip,False),(self.x-9-scroll[0],self.y-9-scroll[1]))

    def getCollisions(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

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