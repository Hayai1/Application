import pygame,math,random
from pygame.locals import *
class Vfx:  
    class BezierArc:
        def __init__(self, start, end, control, color, width,direction='down',x=0,y=0,flip=False,vel=1,revealSpeed=1000):
            self.start = start#start coordinate
            self.end = end#end coordinate
            self.control = control#control coordinate
            self.color = color#color of the arc
            self.width = width#width of the arc
            self.x = x#x position of the arc
            self.y = y#y position of the arc
            self.vel = vel#velocity of the arc
            self.flip = flip#which side to draw them the arc on (left or right)
            self.alphaVelocity = 10#how fast the arc fades out
            self.time = 0#time since the arc was created
            self.direction = direction#direction of the arc
            if self.flip:#if the arc is on the left side of the screen
                self.x = self.x - 32#move the arc to the left
                self.vel = -self.vel#make the arc move to the left
            self.revealSpeed = revealSpeed#how fast the arc reveals itself
            self.revealAmount=3#how much of the arc is revealed
            self.time = 0#time since the arc was created
            self.surf = pygame.Surface((200, 200))#surface to draw the arc on
            self.surf.set_colorkey((0, 0, 0))#set the colorkey to black (so that black is transparent)
            self.firstPoints = self.bezeirCurveEquation(self.control)#get the first set of points
            self.secondaryPoints = self.bezeirCurveEquation((self.control[0]-35,self.control[1]))#get the second set of points

        def draw(self,points,x,y,screen,scroll,yFlip):#draw the arc
            self.surf.fill((0,0,0))#fill the surface with black
            pygame.draw.polygon(self.surf, self.color,points)#draw the arc on the surface
            screen.blit(pygame.transform.flip(pygame.transform.scale(self.surf, (40,40)),self.flip,yFlip),(x-scroll[0],y-16-scroll[1]))#draw the arc surface on the screen
            
        def update(self,x,y,screen,scroll):#update the arc
            if self.flip:x = x - 32#move the arc to the left
            points = self.getPoints()#get the amount of points to show
            if self.direction == 'down':self.draw(points,x,y,screen,scroll,False)#draw the arc where the slash starts from the bottom
            else:self.draw(points,x,y,screen,scroll,True)#draw the arc where the slash starts from the top
            alpha = 255*math.cos(abs(math.radians(self.time*self.alphaVelocity)))#calculate the alpha/opacity value
            self.surf.set_alpha(alpha)#set the alpha/opacity value
            self.time+=1#increase the time
            self.revealAmount=self.revealAmount+1+self.revealSpeed #increase the amount of points to show
            if self.revealAmount > len(self.firstPoints):#if the amount of points to show is greater than the amount of points
                self.revealAmount=len(self.firstPoints)-1#set the amount of points to show to the amount of points
            return self.surf.get_alpha() == 0#return if the arc is finished
            
        def getPoints(self):#get the amount of points to show
            neededFirstPoints = self.firstPoints[:self.revealAmount]#get the first set of points
            neededFirstPoints.reverse()#reverse the first set of points
            points = self.secondaryPoints[:self.revealAmount]+ neededFirstPoints#add the first set of points to the second set of points
            return points#return the points
        
        def bezeirCurveEquation(self,control):#bezier curve equation
            points = []#list of points
            for i in range(0, 1000):#get 1000 t values => 1000 points
                t = i/1000#t value to get t value as a percentage (0-1)
                #bezier curve parametric equations
                x = (1-t)**2*self.start[0] + 2*(1-t)*t*control[0] + t**2*self.end[0]#x value equation
                y = (1-t)**2*self.start[1] + 2*(1-t)*t*control[1] + t**2*self.end[1]#y value equation
                points.append((x, y))#add the point to the list of points
            return points#return the list of points


        
    class particleManagerRain:#particle manager for rain
        def __init__(self):
            self.particles = []#list of particles
            self.timer = 0#timer

        def update(self,gameSurface, scroll):#update the particles
            if self.timer >= 10:#if the timer is greater than 10
                self.timer = 0#reset the timer
                self.newParticle()#create a new particle
            self.timer +=1#increase the timer
            deadParticles = []#list of particles to remove
            for particle in self.particles:#for each particle
                particle.update()#update the particle
                particle.draw(gameSurface,scroll)#draw the particle
            for particlesToRemove in deadParticles:#for each particle to remove
                self.particles.remove(particlesToRemove)#remove the particle
        def newParticle(self):#create a new particle
            self.particles.append(Vfx.Particle([random.uniform(0,1920), 0], [-0.5,0.5],[-0.001,0.001], random.uniform(0.1,1), (125, 249, 255), 100))#add a new particle to the list of particles



    class Particle:#particle class
        def __init__(self, pos, vel, acc, r, color, life):#initialize the particle
            self.pos = pos#position of the particle
            self.vel = vel#velocity of the particle
            self.acc = acc#acceleration of the particle
            self.r = r#radius of the particle
            self.color = color#color of the particle
            self.life = life#life of the particle
            self.accelerationTimer = 0#timer for acceleration
            self.glowDecrease = 2#how much the glow decreases
            self.glow = Vfx.Glow(self.pos)#create a glow for the particle
        def update(self):#update the particle
            self.vel[0] += self.acc[0]+random.uniform(-0.1,0.1)#add the acceleration to the velocity
            self.vel[1] += self.acc[1]# add the acceleration to the velocity
            self.pos[0] += self.vel[0]+random.uniform(-0.1,0.1)#add the velocity to the position
            self.pos[1] += self.vel[1]+random.uniform(-0.1,0.1)#add the velocity to the position
            self.acc[0] = random.uniform(-0.01,0.01)#randomize the acceleration
            if self.accelerationTimer >= 10:#if the acceleration timer is greater than 10
                self.acc[0] = random.uniform(-0.01,0.001)#randomize the acceleration
                self.acc[1] = random.uniform(0,0.001)#randomize the acceleration
                self.accelerationTimer = 0#reset the acceleration timer
            self.life -= 1#decrease the life
        def draw(self,screen,scroll):#draw the particle
            self.glow.draw(screen,scroll,self.r)#draw the glow
            pygame.draw.circle(screen, self.color, (self.pos[0]-scroll[0],self.pos[1]-scroll[1]), self.r)#draw the particle
            

    class Glow:#glow class
        def __init__(self, pos,color=(125, 249, 255)):#initialize the glow
            self.pos = pos#position of the glow
            self.color = color#color of the glow
        def draw(self,screen,scroll,r=0):#draw the glow
            x = 0#x value
            for i in range(0,3):#for each glow
                x += 0.8#increase the x value
                glowDecrease = (math.e**x)#calculate the glow decrease
                screen.blit(self.circle_surf(r,(int(self.color[0]/glowDecrease),int(self.color[1]/glowDecrease),int(self.color[2]/glowDecrease))), 
                        (int(self.pos[0] - r)-scroll[0], int(self.pos[1] - r)-scroll[1]), special_flags=BLEND_RGB_ADD)#draw the glow
                r = r * 2#increase the radius
                
        def circle_surf(self, radius, color):#create a circle surface
            surf = pygame.Surface((radius * 2, radius * 2))#create a surface
            pygame.draw.circle(surf, color, (radius, radius), radius)#draw the circle
            surf.set_colorkey((0, 0, 0))#set the color key
            return surf#return the surface



