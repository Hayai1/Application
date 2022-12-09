import pygame,math,random
from scripts.coreFuncs import *
from pygame.locals import *
class Vfx:
    class Arc:
        '''
        pos : where the curve is 
        radius : lenth of the curve from it's center to its edge 
        spacing : 
        startAngle : the direction the curve will be facing
        speed : 
        curveRate : the rate of curviture 
        scale : size of the curve
        start : where the curve starts from when it's created
        end : where the curve ends at the end of its life
        duration :
        color : colour of the curve
        fade : how fast the curve fades
        arcStretch :how much the curve is stretched out
        widthDecay : how fast the curves width disapears
        motion : how fast the curve moves through the air
        decay :
        angleWidth :
        '''
        def __init__(self, pos, radius, spacing, startAngle, speed, curveRate, scale, start=0, end=1, duration=30, color=(255, 255, 255), fade=0.3, arcStretch=0, widthDecay=50, motion=0, decay=['up', 60], angleWidth=0.2):
            self.startAngle = startAngle
            self.speed = speed
            self.curveRate = curveRate
            self.scale = scale
            self.time = 0
            self.spacing = spacing
            self.radius = radius
            self.angleWidth = angleWidth
            self.shrink = 0
            self.width = 0.05
            self.end = end
            self.start = start
            self.duration = duration
            self.color = color
            self.fade = fade
            self.pos = list(pos)
            self.arcStretch = arcStretch
            self.widthDecay = widthDecay
            self.motion = motion
            self.decay = decay
            self.alive = True

        def getAnglePoint(self, basePoint, t, curveRate):
            p = advance(basePoint.copy(), self.startAngle + (0.5 - t) * math.pi * 4 * self.angleWidth, self.radius)
            advance(p, self.startAngle, (0.5 ** 2 - abs(0.5 - t) ** 2) * self.radius * curveRate)
            if self.arcStretch != 0:
                advance(p, self.startAngle + math.pi / 2, (0.5 - t) * self.arcStretch * self.scale)
            return p

        def calculatePoints(self, start, end, curveRate):
            basePoint = advance([0, 0], self.startAngle, self.spacing)
            pointCount = 20
            arcPoints = [self.getAnglePoint(basePoint, start + (i / pointCount) * (end - start), curveRate) for i in range(pointCount + 1)]
            arcPoints = [[p[0] * self.scale, p[1] * self.scale] for p in arcPoints]
            return arcPoints

        def update(self):
            self.time += self.speed * 0.01
            if self.decay[0] == 'up':
                self.start -= self.start / 20 * 0.01 * self.decay[1]
            elif self.decay[0] == 'down':
                self.end += (1 - self.end) / 20 * 0.01 * self.decay[1]
            self.width += (1 - self.width) / 4 * 0.01 * self.widthDecay
            self.spacing += self.motion * 0.01
            if self.time > self.duration:
                self.alive = False
                return True
            return False

        def render(self, surf, offset=(0, 0)):
            if self.time > 0:
                start = self.start
                end = self.end
                points = self.calculatePoints(start, end, self.curveRate + self.time / 12) + self.calculatePoints(start, end, (self.curveRate + self.time / 12) * self.width)[::-1]
                points = [[p[0] - offset[0] + self.pos[0], p[1] - offset[1] + self.pos[1]] for p in points]
                self.shrink += 10
                for i in range(1,self.shrink):
                    if len(points)-1 > i: 
                        points.pop(i)
                color = [int(self.color[i] - self.color[i] * self.fade * self.time / self.duration) for i in range(3)]
                if color[0] > 255 or color[1] > 255 or color[2] > 255 or color[0] < 0 or color[1] < 0 or color[2] < 0:
                    return False
                pygame.draw.polygon(surf, color, points)


        
    class particleManager:
        def __init__(self,screen):
            self.screen = screen
            self.particles = []
            self.timer = 0

        def update(self,scroll):
            if self.timer >= 10:
                self.timer = 0
                self.newParticle()
            self.timer +=1
            deadParticles = []
            for particle in self.particles:
                particle.update()
                particle.draw(self.screen,scroll)
            for particlesToRemove in deadParticles:
                self.particles.remove(particlesToRemove)
        def newParticle(self):
            self.particles.append(Vfx.Particle([random.uniform(0,1920), 0], [-0.5,0.5],[-0.001,0.001], 1, (125, 249, 255), 100))



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
            
            self.glow.draw(screen,scroll,self.r)
            pygame.draw.circle(screen, self.color, (self.pos[0]-scroll[0],self.pos[1]-scroll[1]), self.r)
        

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
                
            
        def update():
            pass
        def circle_surf(self, radius, color):
            surf = pygame.Surface((radius * 2, radius * 2))
            pygame.draw.circle(surf, color, (radius, radius), radius)
            surf.set_colorkey((0, 0, 0))
            return surf



