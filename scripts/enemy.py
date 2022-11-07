from character import Character
import threading
PLAYER_W = 27
PLAYER_COL = [0,0,200]
JUMP_FORCE = -9
#JUMP_FORCE = -13
GRAVITY = 30
MAX_SPEED = 4
FPS = 60
collidable = (1,2,3)
class Enemy(Character):
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
    def update(self,ai,NODE_THRESHOLD,world1,player1,surface,camera):
        self.triggerJump = False
        if ai.solve != None:
            if (not ai.solve.is_alive()):
                if (ai.path is not None and ai.currentStep/NODE_THRESHOLD < len(ai.path)):
                    if (ai.path[int(ai.currentStep/NODE_THRESHOLD)].y < self.rect.bottom):
                        self.triggerJump = True
                    elif (self.velocity[1] < 0):
                        self.velocity[1] = 0
                    if (ai.path[int(ai.currentStep/NODE_THRESHOLD)].x > self.rect.center[0]):
                        self.velocity[0] = MAX_SPEED
                    elif (ai.path[int(ai.currentStep/NODE_THRESHOLD)].x < self.rect.center[0]):
                        self.velocity[0] = -1*MAX_SPEED
                    else:
                        self.velocity[0] = 0
                    ai.currentStep += 1
                else:
                    self.velocity[0] = 0
                    ai.nextSolve = True
        if ai.nextSolve and player1.inAggroRange(self) and not player1.inAttackRange(self):
            ai.solve = threading.Thread(target=ai.getPath, 
                                    args=(world1.RectPositions, 
                                            (self.rect.y, self.rect.x), 
                                            (player1.rect.y, player1.rect.x)
                                        ,))
            ai.solve.start()
            ai.currentStep = 0
            ai.nextSolve = False
        self.move(world1.rects)
        self.drawPlayer(surface,camera.scroll)
    def jump(self):
        if (not self.triggerJump):
                self.velocity[1] = JUMP_FORCE
                self.triggerJump = True



        