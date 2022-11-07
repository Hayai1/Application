import pygame
import random
BLACK = (0, 0, 0)
collidable = (1,2,3)
class SpriteSheet:
    def __init__(self,spriteSheetFile):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(spriteSheetFile).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {spriteSheetFile}")
            raise SystemExit(e)
    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class Room:
    def __init__(self,roomType,RoomFile,loc):
        self.RoomSpriteSheet = SpriteSheet("assets/spriteSheets/roomSpriteSheet.png")
        self.roomType = roomType
        self.x = loc[0]
        self.y = loc[1]
        self.roomImg = []
        self.rects = []
        self.GenerateRoom(RoomFile)
     
    def getRoomData(self,RoomFile):
        with open(RoomFile) as data:
            return data.read()


    def addImageToArray(self,room,imglocInSpriteSheet,TileLocation):
        room.append([self.RoomSpriteSheet.image_at(imglocInSpriteSheet,BLACK),TileLocation])
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
        
    def genWorld(self):
        for i in range(0,self.roomAmount):
            roomLength = 20
            roomHeight = 8
            xMultiplier = roomLength*16
            yMultiplier = roomHeight*16
            rndNum = random.randint(1,5)
            findingEmptySpace = True
            if rndNum == 1 or rndNum == 2:#left
                newPos = [self.currentPosition[0]-1,self.currentPosition[1]]
                while findingEmptySpace:
                    while findingEmptySpace:
                        findingEmptySpace = False
                        if self.nodes == []:
                            break
                        for room in self.nodes:
                            room = [room[0]/xMultiplier,room[1]/yMultiplier]
                            if newPos == room:
                                newPos = [newPos[0]-1,newPos[1]]
                                findingEmptySpace = True
                                break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.nodes.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    newRoom = Room('1','data/worldData/rooms/1.txt',loc=[(newPos[0]*xMultiplier),newPos[1]*yMultiplier])
                    self.rooms.append(newRoom)
            elif rndNum == 3 or rndNum ==4 :#right
                newPos = [self.currentPosition[0]+1,self.currentPosition[1]]
                while findingEmptySpace:
                    findingEmptySpace = False
                    if self.nodes == []:
                        break
                    for room in self.nodes:
                        room = [room[0]/xMultiplier,room[1]/yMultiplier]
                        if newPos == room:
                            newPos = [newPos[0]+1,newPos[1]]
                            findingEmptySpace = True
                            break
                if newPos[0] >= 0 and newPos[1] >= 0:
                    self.currentPosition = newPos
                    self.nodes.append([newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    newRoom = Room('1','data/worldData/rooms/1.txt',loc=[newPos[0]*xMultiplier,newPos[1]*yMultiplier])
                    self.rooms.append(newRoom)
            elif rndNum == 5:#down
                newPos = [self.currentPosition[0],self.currentPosition[1]+1]
                while findingEmptySpace:
                    findingEmptySpace = False
                    if self.nodes == []:
                        break
                    for room in self.nodes:
                        if newPos == room:
                            newPos = [newPos[0],newPos[1]+1]
                            findingEmptySpace = True
                            break    
                if newPos[0] >= 0 and newPos[1] >= 0:
                    if len(self.rooms)-2 > 0:
                        aboveRoom = self.rooms[len(self.rooms)-1]
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
        
        '''
        there is a bug rigth now with the first couple of rooms so that needs fixing
        '''