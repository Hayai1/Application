
import pygame, time
from scripts.ai import Ai
from scripts.character import Character
class Enemy(Character):
    def __init__(self,x, y, width, height,graph,imgPath,velocity=[],acceleration=[0,0],target=None,surf=None,camera=None,collisionRects=None):
        self.target=target
        self.surf=surf
        self.camera=camera
        self.collisionRects=collisionRects
        self.name ="enemy"
        self.graph = graph
        self.img = pygame.image.load(imgPath)
        self.img.set_colorkey((0,0,0))
        self.ai = Ai(graph)
        self.path = None
        self.nextNode = None   
        self.moving = False
        self.jumping = False
        self.nodePointer = 0
        self.frame = 0
        self.movingFrames = 0
        self.newPathTimer = 0
        super().__init__(x, y, width, height,velocity,acceleration)
        self.currentNode = self.graph.getNodeCloseTo(self)
    def getAnimations(self):
        return NotImplementedError

    def getAggro(self,player):
        if self.x - player.x < 300 and self.x - player.x > -300 and self.y - player.y < 300 and self.y - player.y > -300:
            return True
        return False
        
    def draw(self,screen,scroll):
        screen.blit(self.img, (self.rect.x - scroll[0],self.rect.y - scroll[1]))
    def update(self):
        self.newPathTimer +=1
        #check if a current path exists
        if self.movingFrames == self.frame:
            self.moving = False
        if self.movingFrames < self.frame:#error can occur here
            self.path = None
            self.nodePointer = 0
            self.nextNode = None
            self.frame = 0
        if self.jumping:
            if self.nextNode is not None and self.nextNode.y > self.y:
                self.jumping = False
                if self.nextNode.x > self.currentNode.x:
                    self.left = False
                    self.right = True
                elif self.nextNode.x < self.currentNode.x:
                    self.right = False
                    self.left = True
                self.movingFrames = abs(self.currentNode.getG(self.nextNode)[0]*8)
                self.frame = 0
        condition = self.path == None
        if condition:
            #check if player is in aggro range
            if self.getAggro(self.target):
                #if player is in aggro range then get a path to the player
                self.newPathTimer = 0
                self.path = self.ai.DrawPath(self.graph.getNodeCloseTo(self),self.target)   
            #check if currently in the process from moving to the next node
        else:
            if not self.moving:
                #get the actual node in terms of postion in the graph
                closestNode = self.graph.getNodeCloseTo(self)
                #if the actual node is not the same as the current node then set the path to none and move on
                if self.nodePointer != 0 and closestNode != self.nextNode and self.airTimer < 4:
                    self.path = None
                    self.nodePointer = 0
                    self.nextNode = None
                else:#if the actual node is the same as the current node then get the next node to move to
                    if self.nextNode is None:
                        self.currentNode = self.path[0]
                    else:
                        self.currentNode = self.nextNode
                    self.left = False
                    self.right = False
                    self.nodePointer += 1
                    if self.nodePointer <= len(self.path) - 1:
                        self.nextNode = self.path[self.nodePointer]
                        #using the current node connection to the next node g score to get the next node
                        gScore = self.currentNode.getG(self.nextNode)
                        gScoreX = gScore[0]
                        gScoreY = gScore[1]
                        #state which directions to move in and if jumping is needed
                        if gScoreY != 0 and self.currentNode.y > self.nextNode.y:
                            self.playerJump()
                            self.jumping = True
                            self.movingFrames = 0
                        elif self.nextNode.x > self.currentNode.x:
                            self.left = False
                            self.right = True
                            self.movingFrames = abs(gScoreX*8)
                        elif self.nextNode.x < self.currentNode.x:
                            self.right = False
                            self.left = True
                            self.movingFrames = abs(gScoreX*8)
                        #reset the frame
                        self.frame = 1
                        self.moving = True#state that the enemy is moving
                    else:
                        self.path = None
                        self.nodePointer = 0
                        self.nextNode = None
            else:#if the enemy is moving then move
                self.frame += 1
        
        self.move(self.collisionRects)#call the move function
        self.draw(self.surf,self.camera.scroll)#draw the enemy
        
        
           
    def jump(self):
        if self.airTimer < 6:
            self.acceleration[1] = -5
    