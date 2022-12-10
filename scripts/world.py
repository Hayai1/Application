import pygame
import random

from scripts.vfx import Vfx
from scripts.room import Room

'''
a 1 room = a room with a left and right exit
a 2NoTop = a room with a left, right and bottom exit
a 2Top = a room witha  a left, right bottom and top exit
a 3 = a room with a left, right and top exit
'''
class World:
    def __init__(self,screen,camera,roomAmount):
        self.particleMangager = Vfx.particleManager(screen)
        self.roomAmount = roomAmount
        self.camera = camera
        self.screen = screen
        self.roomLocations = []
        self.rooms = []
        self.rects = []
        self.currentPosition = [0,0]
        self.genWorld()
        self.getRects()

    def getRects(self):
        for room in self.rooms:
            for rect in room.rects:
                self.rects.append(rect)
    
    def update(self):
        for room in self.rooms:
            self.screen.blit(room.roomImg,(room.x-self.camera.scroll[0],room.y-self.camera.scroll[1]))
        self.particleMangager.update(self.camera.scroll)

    def travel(self,pos,xDirection,yDirection,xMultiplier,yMultiplier,):
        pos = [pos[0]+xDirection,pos[1]+yDirection]#move current postion to the left
        if not self.roomLocations == []:
            for room in self.roomLocations:
                room = [room[0]/xMultiplier,room[1]/yMultiplier]
                if pos == room:
                    pos = self.travel(pos,xDirection,yDirection,xMultiplier,yMultiplier)
                    break
        return pos

    def genWorld(self):
        for i in range(0,self.roomAmount):#generate "roomAmount" of rooms
            #length of the room is 20x8 16x16 tiles
            roomLength = 20
            roomHeight = 8
            xMultiplier = roomLength*16
            yMultiplier = roomHeight*16
            #------------------------------->
            #generate a random number to move down or sideways by
            rndNum = random.randint(1,5)
            #--------------------------------------------->
            if rndNum is 1 or rndNum is 2:#if random number is 1 or 2 then place a room to the next empty left postion in the row of rooms
                newPos = self.travel(self.currentPosition,-1,0,xMultiplier,yMultiplier)
                self.currentPosition = newPos
                self.roomLocations.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                newRoom = Room('1','data/worldData/rooms/1.txt',loc=[(newPos[0]*xMultiplier),newPos[1]*yMultiplier])
                for room in self.rooms:
                    if room.x == newPos[0] + xMultiplier and room.y == newPos[1]:
                        room.parent = newRoom
                        break
                self.rooms.append(newRoom)
            elif rndNum is 3 or rndNum  is 4 :#else if random number is 3 or 4 then place a room to the next empty right postion in the row of rooms 
                newPos = self.travel(self.currentPosition,1,0,xMultiplier,yMultiplier)
                self.currentPosition = newPos
                self.roomLocations.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                newRoom = Room('1','data/worldData/rooms/1.txt',loc=[newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                for room in self.rooms:
                    if room.x == newPos[0] + xMultiplier and room.y == newPos[1]:
                        room.parent = newRoom
                        break
                self.rooms.append(newRoom)
            elif rndNum == 5:#else if random number is 5 then place a room directly down
                newPos = self.travel(self.currentPosition,0,1,xMultiplier,yMultiplier)    
                if newPos[0] >= 0 and newPos[1] >= 0:
                    if len(self.rooms)-2 > 0:
                        aboveRoom = self.rooms[-1]
                        if aboveRoom.roomType == '1':
                            newRoom = Room('2NoTop','data/worldData/rooms/2NoTop.txt',loc=[aboveRoom.x,aboveRoom.y])
                            self.rooms[len(self.rooms)-1] = newRoom
                        elif aboveRoom.roomType == '3':
                            newRoom = Room('2Top','data/worldData/rooms/2Top.txt',loc=[aboveRoom.x,aboveRoom.y])
                            self.rooms[len(self.rooms)-1] = newRoom
                    self.currentPosition = newPos
                    self.roomLocations.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    newRoom = Room('3','data/worldData/rooms/3.txt',loc=[newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    self.rooms.append(newRoom)

