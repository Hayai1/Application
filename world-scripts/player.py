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

class Player:
    def __init__(self,x,y,rectsToCollide):
        self.left = False
        self.right = False
        self.triggerJump = False
        self.airTimer = 0
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,16,16)
        self.rectsToCollide = rectsToCollide
    
    def inAggroRange(self,character):
        if abs(self.rect.x - character.rect.x) < 150 and abs(self.rect.y - character.rect.y) < 150:
            return True
        else:
            return False
    def inAttackRange(self,character):
        if abs(self.rect.x - character.rect.x) < 100 and abs(self.rect.y - character.rect.y) < 100:
            return True
        else:
            return False

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

    def move(self,ignoreUPdateVelocity = False):
        collisionTypes = {'top':False,'bottom':False,'right':False,'left':False}
        if self.acceleration[1] < 3:
            self.acceleration[1] += 0.2
        if not ignoreUPdateVelocity:
            self.updateVelocity()
        if self.triggerJump:
            self.playerJump()
        self.rect.x += self.velocity[0]
        collisions = self.getCollisions(self.rectsToCollide)
        for tile in collisions:
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                collisionTypes['right'] = True
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                collisionTypes['left'] = True
        self.rect.y += self.velocity[1]
        collisions = self.getCollisions(self.rectsToCollide)
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
    def moveAi(self, xVel, map):

        #first move left/right
        self.rect.move_ip(xVel, 0)

        #if the new position hits a collidable object...
        #(hits the left side)
        if (self.rect.left < 0 or
            map[int(self.rect.top/32)][int(self.rect.left/32)] in collidable or
            map[int(self.rect.bottom/32)][int(self.rect.left/32)] in collidable):

            #move it back enough pixels to be clear
            self.rect.left += 32 - self.rect.left%32

        #(hits the right side)
        elif (self.rect.right >= len(map[0])*32 or
              map[int(self.rect.top/32)][int(self.rect.right/32)] in collidable or
              map[int(self.rect.bottom/32)][int(self.rect.right/32)] in collidable):
            self.rect.right -= self.rect.right%32 + 1


        #Adjust y coordinate
        self.rect.move_ip(0, self.velocity[1])

        #if it has hit ground...
        if (self.rect.bottom >= len(map)*32 or
            map[int((self.rect.bottom)/32)][int(self.rect.left/32)] in collidable or
            map[int((self.rect.bottom)/32)][int(self.rect.right/32)] in collidable):

            #make sure it doesn't fall through
            #also, now the player is able to jumping
            self.rect.bottom -= self.rect.bottom%32 + 1
            self.yVelocity = 0
            self.triggerJump = False
            
        #if it hits the ceiling...
        elif (self.rect.top < 0 or
              map[int(self.rect.top/32)][int(self.rect.left/32)] in collidable or
              map[int(self.rect.top/32)][int(self.rect.right/32)] in collidable):

            #just make it fall, perhapse reverse its velocity?
            self.rect.top += 32 - self.rect.top%32
            self.yVelocity = 0


        #update the y velocity by the appropriate gravity
        self.velocity[1] += GRAVITY/FPS

        #make sure that if the player is truly falling, he can't jumping
        if (self.velocity[1] > 2*GRAVITY/FPS):
            self.triggerJump = True

        #don't let him fall too fast
        if (self.velocity[1] > 15):
            self.velocity[1] = 10

    def jump(self):
        if (not self.triggerJump):
                self.velocity[1] = JUMP_FORCE
                self.triggerJump = True



        