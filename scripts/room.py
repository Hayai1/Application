import pygame
from scripts.spriteSheet import SpriteSheet

class Room:
    def __init__(self,roomType,RoomFile,loc):
        self.spriteSheet = SpriteSheet("assets/spriteSheets/roomSpriteSheet.png")#the sprite sheet for the rooms
        self.roomType = roomType#the type of room
        self.x = loc[0]#the x location of the room
        self.y = loc[1]#the y location of the room
        self.roomImg = []#the image of the room
        self.collisionRects = []#the collision rects for the room
        self.graphRects = []#the graph rects for the room
        self.GenerateRoom(RoomFile)#generate the room
     
    def getRoomData(self,RoomFile):#getRoomData gets the data from the room file
        with open(RoomFile) as data:#open the room file
            return data.read()#return the data from the room file


    def GetCoordinatesInSpriteSheet(self,Tile,location,ifNum='0'):#this uses recusion to find the location of the tile in the spritesheet
        if ifNum == Tile:#if the tile number is the same as the tile number we are looking for
            return location#return the location
        else:#if the tile number is not the same as the tile number we are looking for
            ifNum = int(ifNum) + 1#add 1 to the tile number
            if location[0] == 64:#if the x location is 64
                location[0] = 0#set the x location to 0
                location[1] += 32#add 32 to the y location
            else:#if the x location is not 64
                location[0] += 32#add 32 to the x location
            return self.GetCoordinatesInSpriteSheet(Tile,location,str(ifNum))#call the function again with the new location and tile number
    def GenerateRoom(self,roomFile):#GenerateRoom generates the room
        room = []#room is a list of the room
        data = self.getRoomData(roomFile)#get the data from the room file
        if self.roomType == '1':#if the room type is 1
            self.collisionRects = [pygame.Rect((self.x,self.y,320,16)),pygame.Rect(self.x,112+self.y,320,16)]#set the collision rects
        elif self.roomType == '2NoTop':#if the room type is 2NoTop
            self.collisionRects = [pygame.Rect((self.x,self.y,320,16)),pygame.Rect(self.x,112+self.y,112,16),#set the collision rects
                                   pygame.Rect(208+self.x,112+self.y,112,16)]
        elif self.roomType == '2Top':#if the room type is 2Top
            self.collisionRects = [pygame.Rect(self.x,self.y,112,16),pygame.Rect(208+self.x,self.y,112,16),#set the collision rects
                                   pygame.Rect(self.x,112+self.y,112,16),pygame.Rect(208+self.x,112+self.y,112,16),
                                   pygame.Rect(112+self.x,64+self.y,96,16)]
        elif self.roomType == '3':#if the room type is 3
            self.collisionRects = [pygame.Rect(self.x,self.y,112,16),pygame.Rect(208+self.x,self.y,112,16),#set the collision rects
                                   pygame.Rect(self.x,112+self.y,320,16),pygame.Rect(112+self.x,64+self.y,96,16)]
        xCounter = -1#set the x counter to -1
        yCounter = 0#set the y counter to 0
        surfaceX = 0#set the surface x to 0
        for tile in data:#for each tile in the data
            xCounter += 1#add 1 to the x counter
            if tile == '\n':#if the tile is a new line
                if surfaceX < xCounter:#if the surface x is less than the x counter
                    surfaceX = xCounter#set the surface x to the x counter
                yCounter +=1#add 1 to the y counter
                xCounter =-1#set the x counter to -1
            else:#if the tile is not a new line
                loc = self.GetCoordinatesInSpriteSheet(Tile=tile,location=[0,0,16,16])#get the location of the tile in the sprite sheet
                room.append([self.spriteSheet.image_at(loc,(0,0,0)),(xCounter*16,yCounter*16)])#add the tile to the room
                if tile != '4':#if the tile is not a 4
                    self.graphRects.append(pygame.Rect((xCounter*16)+self.x,(yCounter*16)+self.y,16,16))#add the tile to the graph rects
        self.roomImg = pygame.Surface((surfaceX*16,yCounter*16+16))#set the room image
        for i in room:#for each tile in the room
            self.roomImg.blit(i[0], i[1])#blit the tile onto the room image
        
        

    def drawRoomOnSurface(self,surface,room):#drawRoomOnSurface draws the room on the surface
        for i in room:#for each tile in the room
            surface.blit(i[0], i[1])#blit the tile onto the surface
        return surface#return the surface
