
import pygame
from scripts.ai import Ai
from scripts.character import Character
class Enemy(Character):
    def __init__(self,x, y, width, height,graph,imgPath,velocity=[],acceleration=[0,0]):
        self.graph = graph
        self.img = pygame.image.load(imgPath)
        self.img.set_colorkey((255,255,255))
        self.ai = Ai(graph)
        self.timeSinceLastSolve = 100
        self.nodePointer = 0
        self.frame = 0
        self.frameToGetNextNode = 16
        self.path = None
        self.solve = False
        self.nextNode = None
        
        super().__init__(x, y, width, height,velocity,acceleration)
        self.currentNode = self.graph.getNodeCloseTo(self)
    def getAnimations(self):
        pass

    def draw(self, screen,scroll,tiles):
        #move based on the path
        cancelCurrentPath = False
        self.left = False
        self.right = False
        if self.path is not None and False:#if a path exists then move based on the path
            if self.currentNode is not None:
                g = self.currentNode.getG(self.nextNode)
                if g is not None:     
                    gx = g[0]
                    gy = g[1]
                    if gy is not 0 and self.currentNode.y > self.nextNode.y :
                        self.jump()
                    if self.nextNode.x > self.currentNode.x:
                        self.left = False
                        self.right = True
                    elif self.nextNode.x < self.currentNode.x:
                        self.right = False
                        self.left = True
                    self.frame += 1
                    self.frameToGetNextNode = 16*abs(gx)
                else:
                    cancelCurrentPath = True
            if self.frame >= self.frameToGetNextNode or cancelCurrentPath:#if frame is equal to the frame to get to the next node then:
                #reset the frame and get the next node to visit
                self.frame = 0
                if self.nodePointer < len(self.path) - 1:#if the ai hasn't reached the last node in the path then get the next node to move too
                    self.nodePointer += 1
                    self.currentNode = self.nextNode
                    self.nextNode = self.path[self.nodePointer]
                else:#else reset the path, the node pointer and the current node
                    self.path = None
                    self.nodePointer = 0
                    self.currentNode = None
                    self.nextNode = None
                    self.nodePointer = 0
        '''
        else:
            self.timeSinceLastSolve += 1
            get to the closest node to make sure the ai doesnt get stuck
            self.currentNode = self.graph.getNodeCloseTo(self)
            self.currentNode.color = (255,0,0)
            if self.currentNode.x > self.rect.x:
                    self.left = False
                    self.right = True
            elif self.currentNode.x < self.rect.x:
                    self.right = False
                    self.left = True#
        '''
        self.move(tiles)
        screen.blit(self.img, (self.rect.x - scroll[0],self.rect.y - scroll[1]))
    def getAggro(self,player):
        if self.x - player.x < 300 and self.x - player.x > -300 and self.y - player.y < 300 and self.y - player.y > -300:
            return True
        return False
        
    def update(self,player):
        
        
        closestNode = self.graph.getNodeCloseTo(self)
        closestNodeToPlayer = self.graph.getNodeCloseTo(player)
        
        
        self.timeSinceLastSolve +=1
        if self.timeSinceLastSolve > 2 and closestNode is not closestNodeToPlayer and self.getAggro(player):
            self.solve = False
            self.path = self.ai.DrawPath(closestNode,player)
            self.path.append(closestNodeToPlayer)
            self.timeSinceLastSolve = 0
            self.nodePointer = 1
            self.nextNode = self.path[self.nodePointer]
           
    def jump(self):
        if self.air_timer < 6:
            self.acceleration[1] = -5
    