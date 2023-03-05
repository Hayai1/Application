import pygame
import random
from scripts.graph import Graph
from scripts.vfx import Vfx
from scripts.room import Room


ROOMSIZE = (20*16,8*16)


class World:
    def __init__(self,name,seed):
        self.particleMangager = Vfx.particleManager()
        self.seed = seed
        self.name = name
        self.rooms = []
        self.currentPosition = [0,0]
        self.genWorld()
        self.collisionRects = self.getRectsToCollideWith()
        self.graph = Graph(self.NodeLocations)
        
    def getDefaultPos(self):
        return [self.rooms[0].graphRects[0].x+8*16,self.rooms[0].graphRects[0].y+16]
    def getRectsToCollideWith(self):
        collisionRects = []
        for room in self.rooms:
            for rect in room.collisionRects:
                collisionRects.append(rect)
        return collisionRects

    @property
    def NodeLocations(self):
        rects = []
        flag = True
        for room in self.rooms:
            if flag:
                flag = False
                continue
            for rect in room.graphRects:
                rects.append([int(rect.x/16),int(rect.y/16)])
        x = [i[0] for i in rects]
        y = [i[1] for i in rects]
        world = [[0 for i in range(max(x)+1)] for j in range(max(y)+1)]
        for rect in rects:
            world[rect[1]][rect[0]] = 1
        return world

    def update(self,gameSurface, scroll):
        for room in self.rooms:
            gameSurface.blit(room.roomImg,(room.x-scroll[0],room.y-scroll[1]))
        self.particleMangager.update(gameSurface,scroll)
        #self.graph.draw(self.screen,self.camera.scroll)
    #-------------------------------------------------------world generation---------------------------------------------------------------------------->
    def travel(self,pos,xDirection,yDirection,):
        pos = [pos[0]+xDirection,pos[1]+yDirection]#move current postion to the left
        if not self.rooms == []:
            for room in self.rooms:
                roomLoc = [room.x,room.y]
                roomLoc = [roomLoc[0]/ROOMSIZE[0],roomLoc[1]/ROOMSIZE[1]]
                if pos == roomLoc:
                    pos = self.travel(pos,xDirection,yDirection)
                    break
        return pos

    def moveSideWays(self,direction):
        if direction == 'left':
            direction = -1
        elif direction == 'right':
            direction = 1
        newPos = self.travel(self.currentPosition,direction,0)
        self.currentPosition = newPos
        if self.currentPosition[0] < 0:
            return self.moveSideWays(-direction)
        newRoom = Room('1','data/worldData/rooms/1.txt',loc=[newPos[0]*ROOMSIZE[0],newPos[1]*ROOMSIZE[1]])
        for room in self.rooms:
            if room.x == newPos[0] + ROOMSIZE[0] and room.y == newPos[1]:
                room.parent = newRoom
                break
        self.rooms.append(newRoom)
    
    def genWorld(self):
        self.rooms.append(Room('1','data/worldData/rooms/1.txt',loc=[0,0]))
        #length of the room is 20x8 16x16 tiles
        
        left = ('1','2')
        right = ('3','4')
        down = ('5')
        for direction in self.seed:#generate "roomAmount" of rooms
            #generate a random number to move down or sideways
            #--------------------------------------------->
            #if random number is 1 or 2 then place a room to the next empty left postion in the row of rooms
            if direction in left:
                #move current postion to the left and place a room to the left
                self.moveSideWays('left')
            #else if random number is 3 or 4 then place a room to the next empty right postion in the row of rooms 
            elif direction in right:
                #move current postion to the right and place a room to the right
                self.moveSideWays('right')
            #else if random number is 5 then place a room directly up
            elif direction in down:
                #move current postion down
                newPos = self.travel(self.currentPosition,0,1)    
                #get the room above the new room
                aboveRoom = self.rooms[-1]
                #if the room above is a 1 then make the new room a 2NoTop
                if aboveRoom.roomType == '1':
                    #change the room above to a 2NoTop
                    self.rooms[-1] = Room('2NoTop','data/worldData/rooms/2NoTop.txt',loc=[aboveRoom.x,aboveRoom.y])
                #if the room above is a 3 then make the new room a 2Top
                elif aboveRoom.roomType == '3':
                    #change the room above to a 2Top
                    self.rooms[-1] = Room('2Top','data/worldData/rooms/2Top.txt',loc=[aboveRoom.x,aboveRoom.y])
                #set the current position to the new position
                self.currentPosition = newPos
                #add a new room to the world
                self.rooms.append(Room('3','data/worldData/rooms/3.txt',loc=[aboveRoom.x,aboveRoom.y+ROOMSIZE[1]]))
            #else if random number is 6 then place a room directly up
            else:
                #move sideways
                self.moveSideWays('right')
         
            
        
        
        

                    

