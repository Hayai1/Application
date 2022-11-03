from turtle import left
import pygame

class Player:
    left = False
    right = False
    jump = False
    airTimer = 0
    velocity = [0,0]
    acceleration = [0,0]

    def __init__(self,x,y):
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
        self.velocity = [0,0]
        if self.acceleration[1] < 3:
            self.acceleration[1] += 0.2
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        if self.left:
            self.velocity[0] -= 2
        if self.right:
            self.velocity[0] += 2
        
    def move(self,tiles):
        collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
        self.updateVelocity()
        if self.jump:
            if self.airTimer < 6:
                self.acceleration[1] = -5
        self.rect.x += self.velocity[0]
        collisions = self.getCollisions(tiles)
        for tile in collisions:
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                collisionTypes['right'] = True
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                collisionTypes['left'] = True
        self.rect.y += self.velocity[1]
        collisions = self.getCollisions(tiles)
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

        