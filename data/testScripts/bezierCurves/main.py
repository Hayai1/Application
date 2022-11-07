
import pygame,sys

mainClock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')

screen = pygame.display.set_mode((500,500),0,32)
curveSurface = pygame.Surface((300,300))
Surface = pygame.Surface((300,300))
class BezierCurve:
    def __init__(self,p0,p1,p2):
        self.x0,self.y0 = p0
        self.x1,self.y1 = p1
        self.x2,self.y2 = p2
        self.curvepos = [0,100]
        self.colour = [255,0,0]
        self.alph = 0
        curveSurface.set_colorkey((0,0,0))
    def lineSlash(self):
        points = [[0,0],[0,100],[100,100],[100,0]]
        return points
    def gencurve(self,constant):
        frontPoints = []
        backPoints = []
        x = [[0,frontPoints],[constant,backPoints]]      
        for i in x:
            t = 0
            while t < 1:
                xVal= (1-t) ** 2 * self.x0 + (1-t) * 2 * t * self.x1 + t * t * self.x2
                yVal= (1-t) ** 2 * self.y0 +(1-t) * 2 * t * (self.y1+i[0]) + t * t * self.y2
                i[1].append([xVal,yVal])
                t+=0.01
        backPoints.reverse()
        for i in backPoints:
            frontPoints.append(i)
        return frontPoints

    def slash(self):
        
        if self.alph != 0:
            self.alph -= 15
        
    def initNewslash(self):
        mousePos = pygame.mouse.get_pos()
        self.alph = 255
        
        self.curvepos = [mousePos[0]-200,mousePos[1]-200]
            
    

curve = BezierCurve([200,100],[200,0],[100,100])#p0, p1 x, p2 x 


points = curve.gencurve(50)#where 50 is the constant


while True:
    screen.fill((0,0,0))
    curveSurface.fill((0,0,0))
    
    
    
    #curve.slash()
    #curveSurface.set_alpha(curve.alph)
    #pygame.draw.polygon(curveSurface,curve.colour,points)
    points = curve.lineSlash()
    pygame.draw.polygon(Surface,curve.colour,points)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            print(curve.x1,curve.y1)   
            curve.initNewslash()
            
    mx,my = pygame.mouse.get_pos()
 
    screen.blit(pygame.transform.rotate(pygame.transform.scale(curveSurface,(400,400)), 270),curve.curvepos)
    pygame.display.update()
    mainClock.tick(60)