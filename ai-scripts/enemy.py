import pygame
import Map

from Map import *
#Player attributes, plus some other globals that shouldn't be here...
PLAYER_W = 27
PLAYER_COL = [0,0,200]
JUMP_FORCE = -9
#JUMP_FORCE = -13
GRAVITY = 30
MAX_SPEED = 4
FPS = 60

class Enemy:
    #Constructor
    def __init__(self,x,y):
        self.location = pygame.Rect(x, y, PLAYER_W, PLAYER_W)
        self.jumping = False
        self.yVelocity = 0

    def __init__(self,x,y,yVelocity):
        self.location = pygame.Rect(x, y, PLAYER_W, PLAYER_W)
        self.jumping = False
        self.yVelocity = yVelocity

    def inAggroRange(self,character):
        if abs(self.location.x - character.location.x) < 150 and abs(self.location.y - character.location.y) < 150:
            return True
        else:
            return False
    def inAttackRange(self,character):
        if abs(self.location.x - character.location.x) < 100 and abs(self.location.y - character.location.y) < 100:
            return True
        else:
            return False
        
    #Draw player to the screen as a rectangle
    def draw(self, screen, view,color):
        pygame.draw.rect(screen, color, [self.location.left - view.left,
                                              self.location.top - view.top,
                                              PLAYER_W, PLAYER_W], 0)

    #Move player left or right and apply gravity,
        #making sure the player does not collide with a wall
    def move(self, xVel, map):

        #first move left/right
        self.location.move_ip(xVel, 0)

        #if the new position hits a collidable object...
        #(hits the left side)
        if (self.location.left < 0 or
            map[int(self.location.top/32)][int(self.location.left/32)] in collidable or
            map[int(self.location.bottom/32)][int(self.location.left/32)] in collidable):

            #move it back enough pixels to be clear
            self.location.left += 32 - self.location.left%32

        #(hits the right side)
        elif (self.location.right >= len(map[0])*32 or
              map[int(self.location.top/32)][int(self.location.right/32)] in collidable or
              map[int(self.location.bottom/32)][int(self.location.right/32)] in collidable):
            self.location.right -= self.location.right%32 + 1


        #Adjust y coordinate
        self.location.move_ip(0, self.yVelocity)

        #if it has hit ground...
        if (self.location.bottom >= len(map)*32 or
            map[int((self.location.bottom)/32)][int(self.location.left/32)] in collidable or
            map[int((self.location.bottom)/32)][int(self.location.right/32)] in collidable):

            #make sure it doesn't fall through
            #also, now the player is able to jumping
            self.location.bottom -= self.location.bottom%32 + 1
            self.yVelocity = 0
            self.jumping = False
            
        #if it hits the ceiling...
        elif (self.location.top < 0 or
              map[int(self.location.top/32)][int(self.location.left/32)] in collidable or
              map[int(self.location.top/32)][int(self.location.right/32)] in collidable):

            #just make it fall, perhapse reverse its velocity?
            self.location.top += 32 - self.location.top%32
            self.yVelocity = 0


        #update the y velocity by the appropriate gravity
        self.yVelocity += GRAVITY/FPS

        #make sure that if the player is truly falling, he can't jumping
        if (self.yVelocity > 2*GRAVITY/FPS):
            self.jumping = True

        #don't let him fall too fast
        if (self.yVelocity > 15):
            self.yVelocity = 10

    def jump(self):
        if (not self.jumping):
                self.yVelocity = JUMP_FORCE
                self.jumping = True

