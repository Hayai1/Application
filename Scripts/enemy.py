import character
from character import Character


class Enemy(Character):
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