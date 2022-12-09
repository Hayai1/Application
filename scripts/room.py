import pygame
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
