import Map

from Map import *

import Player
from Player import *

import copy
from heapq import heappush, heappop

primaryDirections = ['RIGHT', 'UP_RIGHT', 'UP', 'LEFT', 'UP_LEFT']
NODE_THRESHOLD = 5 #number of frames between each node.
                   #(child.g = parent.g + NODE_THRESHOLD)

class Node:
    def __init__(self, x, y, p, g, end, player):
        self.x = int(x)
        self.y = int(y)
        self.h = 2*(abs(self.x - end[1]) + abs(self.y - end[0]))/NODE_THRESHOLD
        self.g = g
        self.p = p
        self.f = self.h+self.g
        self.state = player
        self.destination = end
    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y)
    def __lt__(self, other):
        return (self.f < other.f)
    def _gt__(self, other):
        return (self.f > other.f)
    def __str__(self):
        return "g:"+str(self.g)+ " h:"+str(self.h)+ "; ("+ \
    str(self.state.location.x)+","+str(self.state.location.y)+")"

    def setH(self, h):
        self.h = h
        self.f = h+self.g

    def setG(self, g):
        self.g = g
        self.f = self.h+g

    def setParent(self, p):
        self.p = p

def keyFunction(x):
    return x.f

class solveClass:
    path = []
    pathFound = False
    def solve(self, myMap, start, end):
        t0 = pygame.time.get_ticks()
        #initialize
        openList = []
        closedList = list()
        start = Node(start[1], start[0], 0, 0, end,Player(start[1]-PLAYER_W/2,start[0]-PLAYER_W,0))
        heappush(openList,start)
        done = False
        while not done:
            if (pygame.time.get_ticks() - t0)/1000 > 0.5:
                self.path = []
                return None
            cur = heappop(openList)
            closedList.append(cur)
            for i in primaryDirections:
                nextNode = self.canMove(i, myMap, cur)
                if (nextNode is None):
                    continue
                if (nextNode not in closedList):
                    if (nextNode not in openList):
                        heappush(openList, nextNode)
                    else:
                        if (openList[openList.index(nextNode)].g > nextNode.g):
                            openList[openList.index(nextNode)] = nextNode
            for i in closedList:
                if (abs(i.x - end[1]) < 5 and abs(i.y - end[0]) < 5):
                    done = True
            if (len(openList) == 0):
                break
        self.path = list()
        self.path.append(closedList[len(closedList)-1])
        prev = self.path[0].p
        while (prev != start):
            self.path.append(prev)
            prev = prev.p
        self.path.append(start)
        self.path.reverse()
        t = (pygame.time.get_ticks() - t0)/1000
        print(t, "seconds")
        self.pathFound = True

    def canMove(self, direction, myMap, cur):
        newPlayer = copy.deepcopy(cur.state)
        xVel = 0
        if (direction == 'UP'):
            newPlayer.jump()
        elif (direction == 'UP_LEFT'):
            newPlayer.jump()
            xVel = -1*MAX_SPEED
        elif (direction == 'LEFT'):
            if(newPlayer.yVelocity < 0):
                newPlayer.yVelocity = 0
            xVel = -1*MAX_SPEED
        elif (direction == 'UP_RIGHT'):
            newPlayer.jump()
            xVel = MAX_SPEED
        elif (direction == 'RIGHT'):
            if(newPlayer.yVelocity < 0):
                newPlayer.yVelocity = 0
            xVel = MAX_SPEED
        for i in range(NODE_THRESHOLD):
            newPlayer.move(xVel, myMap)
        if (newPlayer.location.x == cur.state.location.x and
            newPlayer.location.y == cur.state.location.y):
            return None
        newNode = Node(newPlayer.location.center[0], newPlayer.location.bottom, cur, cur.g + NODE_THRESHOLD,cur.destination, newPlayer)
        return newNode





    #TEST STUFF
