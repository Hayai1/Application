import pygame
import random
from scripts.graph import Graph
from scripts.vfx import Vfx
from scripts.room import Room

class World:
    def __init__(self,screen,camera,roomAmount):
        self.particleMangager = Vfx.particleManager(screen)
        self.roomAmount = roomAmount
        self.camera = camera
        self.screen = screen
        self.rooms = []
        self.seed = []
        self.currentPosition = [0,0]
        self.genWorld()
        self.collisionRects = self.getRectsToCollideWith()
        self.graph = Graph(self.WorldIn01)
        

    def getRectsToCollideWith(self):
        collisionRects = []
        for room in self.rooms:
            for rect in room.collisionRects:
                collisionRects.append(rect)
        return collisionRects

    @property
    def WorldIn01(self):
        rects = []
        for room in self.rooms:
            for rect in room.graphRects:
                rects.append([int(rect.x/16),int(rect.y/16)])
        x = [i[0] for i in rects]
        y = [i[1] for i in rects]
        world = [[0 for i in range(max(x)+1)] for j in range(max(y)+1)]
        for rect in rects:
            world[rect[1]][rect[0]] = 1
        return world

    def update(self):
        for room in self.rooms:
            self.screen.blit(room.roomImg,(room.x-self.camera.scroll[0],room.y-self.camera.scroll[1]))
        self.particleMangager.update(self.camera.scroll)
        #self.graph.draw(self.screen,self.camera.scroll)
    #-------------------------------------------------------world generation---------------------------------------------------------------------------->
    def travel(self,pos,xDirection,yDirection,xMultiplier,yMultiplier,):
        pos = [pos[0]+xDirection,pos[1]+yDirection]#move current postion to the left
        if not self.rooms == []:
            for room in self.rooms:
                roomLoc = [room.x,room.y]
                roomLoc = [roomLoc[0]/xMultiplier,roomLoc[1]/yMultiplier]
                if pos == roomLoc:
                    pos = self.travel(pos,xDirection,yDirection,xMultiplier,yMultiplier)
                    break
        return pos

    def moveSideWays(self,xMultiplier,yMultiplier,direction):
        if direction == 'left':
            direction = -1
        elif direction == 'right':
            direction = 1
        newPos = self.travel(self.currentPosition,direction,0,xMultiplier,yMultiplier)
        self.currentPosition = newPos
        if self.currentPosition[0] < 0:
            return self.moveSideWays(xMultiplier,yMultiplier,-direction)
        newRoom = Room('1','data/worldData/rooms/1.txt',loc=[newPos[0]*xMultiplier,newPos[1]*yMultiplier])
        for room in self.rooms:
            if room.x == newPos[0] + xMultiplier and room.y == newPos[1]:
                room.parent = newRoom
                break
        self.rooms.append(newRoom)
    
    def genWorld(self):
        self.rooms.append(Room('1','data/worldData/rooms/1.txt',loc=[0,0]))
        #length of the room is 20x8 16x16 tiles
        roomLength = 20
        roomHeight = 8
        xMultiplier = roomLength*16
        yMultiplier = roomHeight*16
        left = (1,2)
        right = (3,4)
        down = (5,)
        for i in range(0,self.roomAmount):#generate "roomAmount" of rooms
            #generate a random number to move down or sideways
            rndNum = random.randint(1,5)
            self.seed.append(rndNum)
            #--------------------------------------------->
            if rndNum in left:#if random number is 1 or 2 then place a room to the next empty left postion in the row of rooms
                self.moveSideWays(xMultiplier,yMultiplier,'left')
            elif rndNum in right:#else if random number is 3 or 4 then place a room to the next empty right postion in the row of rooms 
                self.moveSideWays(xMultiplier,yMultiplier,'right')
            elif rndNum in down:#else if random number is 5 then place a room directly down
                newPos = self.travel(self.currentPosition,0,1,xMultiplier,yMultiplier)    
                aboveRoom = self.rooms[-1]
                if aboveRoom.roomType == '1':
                    self.rooms[-1] = Room('2NoTop','data/worldData/rooms/2NoTop.txt',loc=[aboveRoom.x,aboveRoom.y])
                elif aboveRoom.roomType == '3':
                    self.rooms[-1] = Room('2Top','data/worldData/rooms/2Top.txt',loc=[aboveRoom.x,aboveRoom.y])
                self.currentPosition = newPos
                self.rooms.append(Room('3','data/worldData/rooms/3.txt',loc=[aboveRoom.x,aboveRoom.y+yMultiplier]))
            else:
                self.moveSideWays(xMultiplier,yMultiplier,'right')
        
        
        

                    

