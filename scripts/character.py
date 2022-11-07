import pygame
#Player attributes, plus some other globals that shouldn't be here...
PLAYER_W = 27
PLAYER_COL = [0,0,200]
JUMP_FORCE = -9
#JUMP_FORCE = -13
GRAVITY = 30
MAX_SPEED = 4
FPS = 60
collidable = (1,2,3)

class Character:
    def __init__(self,x,y):
        self.left = False
        self.right = False
        self.triggerJump = False
        self.airTimer = 0
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,16,16)
    
    

    def drawPlayer(self,surface,scroll):
        pygame.draw.rect(surface,(0,0,255),pygame.Rect(self.rect.x-scroll[0],self.rect.y-scroll[1],self.rect.width,self.rect.height))
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
            self.acceleration[1] = -5

    def move(self,rectsToCollide,ignoreUPdateVelocity = False):
        collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
        if self.acceleration[1] < 3:
            self.acceleration[1] += 0.2
        if not ignoreUPdateVelocity:
            self.updateVelocity()
        if self.triggerJump:
            self.playerJump()
        self.rect.x += self.velocity[0]
        collisions = self.getCollisions(rectsToCollide)
        for tile in collisions:
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                collisionTypes['right'] = True
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                collisionTypes['left'] = True
        self.rect.y += self.velocity[1]
        collisions = self.getCollisions(rectsToCollide)
        for tile in collisions:
            if self.velocity[1] > 0:
                self.rect.bottom = tile.top
                collisionTypes['bottom'] = True
            elif self.velocity[1] < 0:
                self.rect.top = tile.bottom
                collisionTypes['top'] = True  
        if collisionTypes['bottom']:
            self.airTimer = 0
            self.acceleration = [0,0]
        elif collisionTypes['top']:
            self.acceleration = [0,0]
        else:
            self.airTimer += 1
        self.velocity = [0,0]