from scripts.graph import Graph
from scripts.vfx import Vfx
from scripts.room import Room


ROOMSIZE = (20*16,8*16)#(width,height)


class World:
    def __init__(self,name,seed):#seed is a list of numbers that will be used to generate the world
        self.particleMangager = Vfx.particleManagerRain()
        self.seed = seed#seed is a list of numbers that will be used to generate the world
        self.name = name#name is the name of the world
        self.rooms = []#rooms is a list of rooms
        self.currentPosition = [0,0]#currentPosition is the position of the last place room
        self.genWorld()#genWorld generates the world
        self.collisionRects = self.getRectsToCollideWith()#collisionRects is a list of rects that the player can collide with
        self.graph = Graph(self.NodeLocations)#graph is a graph of the world
        
    def getDefaultPos(self):#getDefaultPos returns the default position of the player
        return [self.rooms[0].graphRects[0].x+8*16,self.rooms[0].graphRects[0].y+16]
    
    def getRectsToCollideWith(self):#getRectsToCollideWith returns a list of rects that the player can collide with
        collisionRects = []#collisionRects is a list of rects that the player can collide with
        for room in self.rooms:#for each room in the world
            for rect in room.collisionRects:#for each rect in the room
                collisionRects.append(rect)#add the rect to the list of rects to collide with
        return collisionRects#return the list of rects to collide with

    @property
    def NodeLocations(self):#NodeLocations return the list of 1 and 0 where 1 is a node and 0 is not a node
        rects = []#rects is a list of the locations of the nodes in the world
        flag = True#flag is a flag that is used to skip the first room
        for room in self.rooms:#for each room in the world
            if flag:#if the flag is true
                flag = False#set the flag to false
                continue#skip the first room
            for rect in room.graphRects:#for each rect in the room
                rects.append([int(rect.x/16),int(rect.y/16)])#add the rect to the list of rects to collide with
        x = [i[0] for i in rects]#x is a list of the x values of the rects
        y = [i[1] for i in rects]#y is a list of the y values of the rects
        world = [[0 for i in range(max(x)+1)] for j in range(max(y)+1)]#world is a 2d list of 0s
        for rect in rects:#for each rect in the list of rects
            world[rect[1]][rect[0]] = 1#set the value in the x,y postion of the rect in the array of 0s (world) to 1
        return world#return the list of 1 and 0 where 1 is a node and 0 is not a node

    def update(self,gameSurface, scroll):#update updates the world
        for room in self.rooms:#for each room in the world
            gameSurface.blit(room.roomImg,(room.x-scroll[0],room.y-scroll[1]))#draw the room to the screen
        self.particleMangager.update(gameSurface,scroll)#update the particle manager
    #-------------------------------------------------------world generation---------------------------------------------------------------------------->
    def travel(self,pos,xDirection,yDirection,):#travel finds an empty location to place a room in a specific direction
        pos = [pos[0]+xDirection,pos[1]+yDirection]#move current postion to the left
        if not self.rooms == []:#if there are rooms in the world
            for room in self.rooms:#for each room in the world
                roomLoc = [room.x,room.y]#get the location of the room
                roomLoc = [roomLoc[0]/ROOMSIZE[0],roomLoc[1]/ROOMSIZE[1]]#scale up the x,y values to the correct size
                if pos == roomLoc:#if the there is a room in this location
                    pos = self.travel(pos,xDirection,yDirection)#move to the next possible room placement location
                    break#break out of the loop
        return pos#return the position of the room to be placed

    def moveSideWays(self,direction):#finds a empty location in the direction left or right to place a room
        if direction == 'left':#if the direction is left
            direction = -1#set the direction to -1
        elif direction == 'right':#if the direction is right
            direction = 1#set the direction to 1
        newPos = self.travel(self.currentPosition,direction,0)#find an empty location to place a room in the direction left or right
        self.currentPosition = newPos#set the current position to the new position
        if self.currentPosition[0] < 0:#if the current position is less than 0
            return self.moveSideWays(-direction)#as we do not want to go into negative x and y change direction and move the oppisite way
        newRoom = Room('1','data/worldData/rooms/1.txt',loc=[newPos[0]*ROOMSIZE[0],newPos[1]*ROOMSIZE[1]])#create a new room
        self.rooms.append(newRoom)#add the new room to the world
    
    def genWorld(self):#genWorld generates the world
        self.rooms.append(Room('1','data/worldData/rooms/1.txt',loc=[0,0]))#add the first room to the world
        left = ('1','2')#left is the tuple of numbers that each detnotes to move left
        right = ('3','4')#right is the tuple of numbers that each detnotes to move right
        down = ('5')#down is the tuple of numbers that each detnotes to move down
        for direction in self.seed:#get the direction from the seed

            #if direction is 1 or 2 then place a room to the next empty left postion in the row of rooms
            if direction in left:
                #move current postion to the left and place a room to the left
                self.moveSideWays('left')
            #else if direction is 3 or 4 then place a room to the next empty right postion in the row of rooms 
            elif direction in right:
                #move current postion to the right and place a room to the right
                self.moveSideWays('right')
            #else if direction is 5 then place a room directly up
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
         
            
        
        
        

                    

