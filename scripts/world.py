import pygame
import random
from scripts.spriteSheet import SpriteSheet
class Room:
    def __init__(self,roomType,RoomFile,loc):
        self.spriteSheet = SpriteSheet("assets/spriteSheets/roomSpriteSheet.png")
        self.roomType = roomType
        self.x = loc[0]
        self.y = loc[1]
        self.roomImg = []
        self.rects = []
        self.parent = None
        self.GenerateRoom(RoomFile)
     
    def getRoomData(self,RoomFile):
        with open(RoomFile) as data:
            return data.read()


    def addImageToArray(self,room,imglocInSpriteSheet,TileLocation):
        room.append([self.spriteSheet.image_at(imglocInSpriteSheet,(0,0,0)),TileLocation])
        return room

    def GetCoordinatesInSpriteSheet(self,Tile,location,ifNum='0'):#this uses recusion to find the location of the tile in the spritesheet
        if ifNum == Tile:
            return location
        else:
            ifNum = int(ifNum) + 1
            if location[0] == 64:
                location[0] = 0
                location[1] += 32
            else:
                location[0] += 32
            return self.GetCoordinatesInSpriteSheet(Tile,location,str(ifNum))
    def GenerateRoom(self,roomFile):
        room = []
        data = self.getRoomData(roomFile)
        xCounter = -1
        yCounter = 0
        surfaceX = 0
        for tile in data:
            xCounter += 1
            if tile == '\n':
                if surfaceX < xCounter:
                    surfaceX = xCounter
                yCounter +=1
                xCounter =-1
            else:
                loc = self.GetCoordinatesInSpriteSheet(Tile=tile,location=[0,0,16,16])
                self.addImageToArray(room,loc,(xCounter*16,yCounter*16))
                if tile != '4':
                    self.rects.append(pygame.Rect((xCounter*16)+self.x,(yCounter*16)+self.y,16,16))
        surface = pygame.Surface((surfaceX*16,yCounter*16+16))
        self.roomImg = self.drawRoomOnSurface(surface,room)

    def drawRoomOnSurface(self,surface,room):
        for i in room:
            surface.blit(i[0], i[1])
        return surface


'''
a 1 room = a room with a left and right exit
a 2NoTop = a room with a left, right and bottom exit
a 2Top = a room witha  a left, right bottom and top exit
a 3 = a room with a left, right and top exit
'''
class World:
    nodes = []
    rooms = []
    currentPosition = [0,0]
    def __init__(self,roomAmount):
        self.roomAmount = roomAmount
        self.genWorld()
        self.RectPositions = self.WorldIn01
        self.rects = []
        for room in self.rooms:
            for rect in room.rects:
                self.rects.append(rect)
    def update(self,surface, camera):
        for room in self.rooms:
            surface.blit(room.roomImg,(room.x-camera.scroll[0],room.y-camera.scroll[1]))
    @property
    def WorldIn01(self):
        rects = []
        for room in self.rooms:
            for rect in room.rects:
                rects.append([int(rect.x/16),int(rect.y/16)])
        x = [i[0] for i in rects]
        y = [i[1] for i in rects]

        world = [[4 for i in range(max(x)+1)] for j in range(max(y)+1)]

        for rect in rects:
            world[rect[1]][rect[0]] = 3
        return world

    def travel(self,pos,xDirection,yDirection,xMultiplier,yMultiplier,):
        pos = [pos[0]+xDirection,pos[1]+yDirection]#move current postion to the left
        if not self.nodes == []:
            for room in self.nodes:
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
                self.nodes.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                newRoom = Room('1','data/worldData/rooms/1.txt',loc=[(newPos[0]*xMultiplier),newPos[1]*yMultiplier])
                for room in self.rooms:
                    if room.x == newPos[0] + xMultiplier and room.y == newPos[1]:
                        room.parent = newRoom
                        break
                self.rooms.append(newRoom)
            elif rndNum is 3 or rndNum  is 4 :#else if random number is 3 or 4 then place a room to the next empty right postion in the row of rooms 
                newPos = self.travel(self.currentPosition,1,0,xMultiplier,yMultiplier)
                self.currentPosition = newPos
                self.nodes.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
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
                    self.nodes.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    newRoom = Room('3','data/worldData/rooms/3.txt',loc=[newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    self.rooms.append(newRoom)

