import character
from character import Character
import threading

class Enemy(Character):
    currentStep = 0
    nextSolve = False
    def __init__(self,rects,playerWidth):
        self.start = [0,0]
        self.end = [0,0]
        self.start[0] = (int(self.start[0])*32)+playerWidth
        self.start[1] = (int(self.start[1])*32)+playerWidth/2
        self.end[0] = (int(self.end[0])*32)+32
        self.end[1] = (int(self.end[1])*32)+16
        super().__init__(x=self.start[0],y=self.start[1],rects=rects,playerWidth=playerWidth)

    def update(self,solveObj, solve, NODE_THRESHOLD,player1,s,rects,surface,scroll):
        self.triggerJump = False
        if (not solve.is_alive()):
            if (solveObj.path is not None and self.currentStep/NODE_THRESHOLD < len(solveObj.path)):
                if (solveObj.path[int(self.currentStep/NODE_THRESHOLD)].y < self.rect.bottom):
                    self.triggerJump = True
                elif (self.velocity[1] < 0):
                    self.velocity[1] = 0
                if (solveObj.path[int(self.currentStep/NODE_THRESHOLD)].x > self.rect.center[0]):
                    self.velocity[0] =  self.MAX_SPEED
                elif (solveObj.path[int(self.currentStep/NODE_THRESHOLD)].x < self.rect.center[0]):
                    self.velocity[0] = -1*self.MAX_SPEED
                else:
                    self.velocity[0] = 0
                self.currentStep += 1
            else:
                self.velocity[0] = 0
                self.nextSolve = True
        if self.nextSolve and player1.inAggroRange(self) and not player1.inAttackRange(self):
            solve = threading.Thread(target=solveObj.solve, args=(s, (self.rect.y, self.rect.x), (player1.rect.y, player1.rect.x), rects,))
            solve.start()
            self.currentStep = 0
            self.nextSolve = False
        self.move()
        self.drawPlayer(surface,scroll)
    def moveAi(self, xVel, map):

        #first move left/right
        self.rect.move_ip(xVel, 0)

        #if the new position hits a collidable object...
        #(hits the left side)
        if (self.rect.left < 0 or
            map[int(self.rect.top/32)][int(self.rect.left/32)] in self.collidable or
            map[int(self.rect.bottom/32)][int(self.rect.left/32)] in self.collidable):

            #move it back enough pixels to be clear
            self.rect.left += 32 - self.rect.left%32

        #(hits the right side)
        elif (self.rect.right >= len(map[0])*32 or
              map[int(self.rect.top/32)][int(self.rect.right/32)] in self.collidable or
              map[int(self.rect.bottom/32)][int(self.rect.right/32)] in self.collidable):
            self.rect.right -= self.rect.right%32 + 1


        #Adjust y coordinate
        self.rect.move_ip(0, self.velocity[1])

        #if it has hit ground...
        if (self.rect.bottom >= len(map)*32 or
            map[int((self.rect.bottom)/32)][int(self.rect.left/32)] in self.collidable or
            map[int((self.rect.bottom)/32)][int(self.rect.right/32)] in self.collidable):

            #make sure it doesn't fall through
            #also, now the player is able to jumping
            self.rect.bottom -= self.rect.bottom%32 + 1
            self.yVelocity = 0
            self.triggerJump = False
            
        #if it hits the ceiling...
        elif (self.rect.top < 0 or
              map[int(self.rect.top/32)][int(self.rect.left/32)] in self.collidable or
              map[int(self.rect.top/32)][int(self.rect.right/32)] in self.collidable):

            #just make it fall, perhapse reverse its velocity?
            self.rect.top += 32 - self.rect.top%32
            self.yVelocity = 0


        #update the y velocity by the appropriate gravity
        self.velocity[1] += self.GRAVITY/self.FPS

        #make sure that if the player is truly falling, he can't jumping
        if (self.velocity[1] > 2*self.GRAVITY/self.FPS):
            self.triggerJump = True

        #don't let him fall too fast
        if (self.velocity[1] > 15):
            self.velocity[1] = 10

    def jump(self):
        if (not self.triggerJump):
                self.velocity[1] = self.JUMP_FORCE
                self.triggerJump = True