import pygame
from scripts.node import Node
import math
class Graph:
    def __init__(self,mapdata):
        self.nodes = self.getNodes(mapdata)
    #draw the graph (nodes and there connections)
    def draw(self,screen,scroll):
        for node in self.nodes:
            pygame.draw.rect(screen,node.color,pygame.Rect(node.x-scroll[0],node.y-scroll[1],3,3))
            coords = [[node.x-scroll[0],node.y-scroll[1]]]
            for connection in node.connections:
                coords.append([connection['node'].x-scroll[0],connection['node'].y-scroll[1]])
                pygame.draw.lines(screen,(255,0,0),False,coords,1)
                coords = [[node.x-scroll[0],node.y-scroll[1]]]
    #returns the node closest to the player
    def getNodeCloseTo(self,player):
        closestNode = None
        for node in self.nodes:
            if closestNode == None:
                closestNode = node
            else:
                distFromCurrentClosestNodeToPlayer = math.sqrt((closestNode.x - player.x)**2 + (closestNode.y - player.y)**2)
                distFromNewNodeToPlayer = math.sqrt((node.x - player.x)**2 + (node.y - player.y)**2)
                if distFromNewNodeToPlayer < distFromCurrentClosestNodeToPlayer:
                    closestNode = node
        closestNode.color = (0,255,0)
        return closestNode

    def getRelativeStateOfNode(self,currentX,currentY,x,y,mapdata):#get the state of a node relative to the current node
        if len(mapdata)-1 < currentY+y or len(mapdata[currentY+y])-1 < currentX+x:
            return None
        else:
            return mapdata[currentY+y][currentX+x]
    #returns a list of nodes created relative to the map passed in
    def getNodes(self,mapdata):
        nodes = []
        x = 0
        y = 0
        id = 0
        for row in mapdata:
            nodeRow = []
            for tile in row:
                if tile !=3:
                    nodeRow.append(None)
                if tile == 3:
                    nodeRow.append(Node(id,x*16+8,y*16))
                    id +=1
                x += 1
            x = 0
            y +=1
            nodes.append(nodeRow)
        #connections
        amountOfRowsOfNodes = len(nodes)#get the amount of rows in nodes
        for rowIndex in range(0, amountOfRowsOfNodes):#loop through each row in nodes
            row = nodes[rowIndex]#get the row
            amountOfNodesInRow = len(row)#get the amount of nodes in the row
            for nodeIndex in range(0, amountOfNodesInRow):#loop through each node in the row
                node = row[nodeIndex]#get the node
                if node is not None:
                    '''<---make connections on the same y levels:--->'''
                    if (nodeIndex is not amountOfNodesInRow-1 and self.getRelativeStateOfNode(nodeIndex,rowIndex,1,0,nodes) is not None):
                        node.add_connection(row[nodeIndex+1],[1,0])
                    if nodeIndex is not 0 and self.getRelativeStateOfNode(nodeIndex,rowIndex,-1,0,nodes) is not None:
                        node.add_connection(row[nodeIndex-1],[1,0])
                    '''<---make connections on different y levels:--->'''
                    #check if there is a node above the current node by 1 and 2
                    if (self.getRelativeStateOfNode(nodeIndex,rowIndex,0,-1,nodes) is None and#is there no node above by 1
                        self.getRelativeStateOfNode(nodeIndex,rowIndex,0,-2,nodes) is None):#is there no node above by 2
                        #if so look for possible connections to make
                        ConnectionYRange = 7#the range of y values to check for nodes
                        ConnectionXRange = 2#the range of x values to check for nodes
                        for y in range(1,ConnectionYRange):#loop through the y range
                            for x in range(-ConnectionXRange,ConnectionXRange+1):#loop through the x range
                                if abs(x) ==0 or abs(x) == 1:continue
                                possibleConnection = self.getRelativeStateOfNode(nodeIndex,rowIndex,x,y,nodes)#get the node at the current x and y
                                if possibleConnection is not None:#if there is a possible connection
                                    #check for nodes that could obstuct the connection:
                                    if (x > 0 and self.getRelativeStateOfNode(nodeIndex,rowIndex,1,0,nodes) is None or x < 0 and self.getRelativeStateOfNode(nodeIndex,rowIndex,-1,0,nodes) is None):
                                        #make a connection
                                        node.add_connection(possibleConnection,[x,y])
        
        nodelist = []
        for row in nodes:
            for node in row:
                if node is not None:
                    nodelist.append(node)
        return nodelist
                            
                                    

