import pygame

import time

'''
create a class called arc that will generate a bazir curve
'''

class Arc:
    
        def __init__(self,screen, start, end, control, color, width,x=0,y=0,vel=4,acl=0.01,revealSpeed=80):
            self.screen = screen
            self.start = start
            self.end = end
            self.control = control
            self.color = color
            self.width = width
            self.x = x
            self.y = y
            self.vel = vel
            self.acl = acl
            self.revealSpeed = revealSpeed
            self.revealAmount=3
            self.time = 0
            self.surf = pygame.Surface((200, 200))
            self.surf.set_colorkey((0, 0, 0))
            self.firstPoints = self.bezeirCurveEquation(self.control)
            self.secondaryPoints = self.bezeirCurveEquation((self.control[0]-100,self.control[1]))


        def draw(self):
            self.surf.fill((0,0,0))
            
            points = self.getPoints()

            
            pygame.draw.polygon(self.surf, self.color,points)


            
            self.screen.blit(arc.surf,(self.x,self.y))
            
        def update(self):
            self.draw()
            self.surf.set_alpha(255-self.time*(self.vel*2))
            self.time+=1
            self.revealAmount=self.revealAmount+1+self.revealSpeed 
            if self.revealAmount > len(self.firstPoints):
                self.revealAmount=len(self.firstPoints)-1
            self.vel = abs(self.vel - self.acl)
            self.x +=self.vel
            
        def getPoints(self):
            neededFirstPoints = self.firstPoints[:self.revealAmount]
            neededFirstPoints.reverse()
            TempSecondaryPointsCopy = self.secondaryPoints.copy()
            lastPoint = self.firstPoints[self.revealAmount-1]
            TempSecondaryPointsCopy[self.revealAmount-1] = lastPoint
            points = TempSecondaryPointsCopy[:self.revealAmount]+ neededFirstPoints
            return points
        def bezeirCurveEquation(self,control):
            points = []
            for i in range(0, 1000):
                t = i/1000
                x = (1-t)**2*self.start[0] + 2*(1-t)*t*control[0] + t**2*self.end[0]
                y = (1-t)**2*self.start[1] + 2*(1-t)*t*control[1] + t**2*self.end[1]
                points.append((x, y))
            
            return points


'''
create base pygame project
'''

pygame.init()

screen = pygame.display.set_mode((800, 600))

arc = Arc(screen,(0, 0), (0, 200), (200, 100), (255, 255, 255), 5)
surf = pygame.Surface((200,200))
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    arc.update()
    
    pygame.display.update()

    clock.tick(60)
