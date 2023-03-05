import pygame,math,random
from pygame.locals import *
class Vfx:  
    class BezierArc:
        def __init__(self, start, end, control, color, width,direction='down',x=0,y=0,flip=False,vel=1,acl=0.01,revealSpeed=1000):
            self.start = start
            self.end = end
            self.control = control
            self.color = color
            self.width = width
            self.x = x
            self.y = y
            self.vel = vel
            self.acl = acl
            self.flip = flip
            self.alphaVelocity = 10
            self.time = 0
            self.direction = direction
            if self.flip:
                self.x = self.x - 32
                self.vel = -self.vel
                self.acl = -self.acl
            self.revealSpeed = revealSpeed
            self.revealAmount=3
            self.time = 0
            self.surf = pygame.Surface((200, 200))
            self.surf.set_colorkey((0, 0, 0))
            self.firstPoints = self.bezeirCurveEquation(self.control)
            self.secondaryPoints = self.bezeirCurveEquation((self.control[0]-35,self.control[1]))

        def draw(self,points,x,y,screen,scroll,yFlip):
            self.surf.fill((0,0,0))
            pygame.draw.polygon(self.surf, self.color,points)
            screen.blit(pygame.transform.flip(pygame.transform.scale(self.surf, (40,40)),self.flip,yFlip),(x-scroll[0],y-16-scroll[1]))
            
        def update(self,x,y,screen,scroll):
            if self.flip:x = x - 32
            points = self.getPoints()
            if self.direction == 'down':self.draw(points,x,y,screen,scroll,False)
            else:self.draw(points,x,y,screen,scroll,True)
            alpha = 255*math.cos(abs(math.radians(self.time*self.alphaVelocity)))
            self.surf.set_alpha(alpha)
            self.time+=1
            self.revealAmount=self.revealAmount+1+self.revealSpeed 
            if self.revealAmount > len(self.firstPoints):
                self.revealAmount=len(self.firstPoints)-1
            return self.surf.get_alpha() == 0
            
        def getPoints(self):
            neededFirstPoints = self.firstPoints[:self.revealAmount]
            neededFirstPoints.reverse()
            points = self.secondaryPoints[:self.revealAmount]+ neededFirstPoints
            return points
        
        def bezeirCurveEquation(self,control):
            points = []
            for i in range(0, 1000):
                t = i/1000
                x = (1-t)**2*self.start[0] + 2*(1-t)*t*control[0] + t**2*self.end[0]
                y = (1-t)**2*self.start[1] + 2*(1-t)*t*control[1] + t**2*self.end[1]
                points.append((x, y))
            return points

        

        
    class particleManager:
        def __init__(self):
            self.particles = []
            self.timer = 0

        def update(self,gameSurface, scroll):
            if self.timer >= 10:
                self.timer = 0
                self.newParticle()
            self.timer +=1
            deadParticles = []
            for particle in self.particles:
                particle.update()
                particle.draw(gameSurface,scroll)
            for particlesToRemove in deadParticles:
                self.particles.remove(particlesToRemove)
        def newParticle(self):
            self.particles.append(Vfx.Particle([random.uniform(0,1920), 0], [-0.5,0.5],[-0.001,0.001], random.uniform(0.1,1), (125, 249, 255), 100))



    class Particle:
        def __init__(self, pos, vel, acc, r, color, life):
            self.pos = pos
            self.vel = vel
            self.acc = acc
            self.r = r
            self.color = color
            self.life = life
            self.accelerationTimer = 0
            self.glowDecrease = 2
            self.glow = Vfx.Glow(self.pos)
        def update(self):
            self.vel[0] += self.acc[0]+random.uniform(-0.1,0.1)
            self.vel[1] += self.acc[1]
            self.pos[0] += self.vel[0]+random.uniform(-0.1,0.1)
            self.pos[1] += self.vel[1]+random.uniform(-0.1,0.1)
            self.acc[0] = random.uniform(-0.01,0.01)
            if self.accelerationTimer >= 10:
                self.acc[0] = random.uniform(-0.01,0.001)
                self.acc[1] = random.uniform(0,0.001)
                self.accelerationTimer = 0
            self.life -= 1
        def draw(self,screen,scroll):
            pygame.draw.circle(screen, self.color, (self.pos[0]-scroll[0],self.pos[1]-scroll[1]), self.r)
            self.glow.draw(screen,scroll,self.r)

    class Glow:
        def __init__(self, pos,color=(125, 249, 255)):
            self.pos = pos
            self.color = color
        def draw(self,screen,scroll,r=0):
            x = 0
            for i in range(0,3):
                x += 0.8
                glowDecrease = (math.e**x)
                screen.blit(self.circle_surf(r,(int(self.color[0]/glowDecrease),int(self.color[1]/glowDecrease),int(self.color[2]/glowDecrease))), 
                        (int(self.pos[0] - r)-scroll[0], int(self.pos[1] - r)-scroll[1]), special_flags=BLEND_RGB_ADD)
                r = r * 2
                
        def circle_surf(self, radius, color):
            surf = pygame.Surface((radius * 2, radius * 2))
            pygame.draw.circle(surf, color, (radius, radius), radius)
            surf.set_colorkey((0, 0, 0))
            return surf



