from scripts.node import Node
import math
class Graph:
    def __init__(self,mapdata):#create the graph
        self.nodes = self.getNodes(mapdata)#get the nodes
                
    #returns the node closest to the player
    def getNodeCloseTo(self,entity):#get the node closest to the argument entity
        closestNode = None#the closest node to the player
        for node in self.nodes:#loop through each node
            if closestNode == None:#if there is no closest node yet
                closestNode = node#set the closest node to the current node

                distFromCurrentClosestNodeToPlayer = math.sqrt((node.x - (entity.x + entity.width/2))**2 + (node.y - (entity.y+entity.height))**2)#get the distance from the current closest node to the player using pythagores theorem
            else:
                distFromNewNodeToPlayer = math.sqrt((node.x - (entity.x + entity.width/2))**2 + (node.y - (entity.y+entity.height))**2)#get the distance from the new node to the player using pythagores theorem
                if distFromNewNodeToPlayer < distFromCurrentClosestNodeToPlayer:#if the new node is closer to the player than the current closest node
                    closestNode = node#set the closest node to the new node
                    distFromCurrentClosestNodeToPlayer = distFromNewNodeToPlayer#set the distance from the current closest node to the player to the distance from the new node to the player
        closestNode.color = (0,255,0)#set the color of the closest node to green (for testing)
        return closestNode#return the closest node

    def getRelativeStateOfNode(self,currentX,currentY,x,y,mapdata):#get the state of a node relative to the current node
        if len(mapdata)-1 < currentY+y or len(mapdata[currentY+y])-1 < currentX+x:#if the node is out of bounds
            return None#return none
        else:#if the node is in bounds
            return mapdata[currentY+y][currentX+x]#return the state of the node
    #returns a list of nodes created relative to the map passed in
    def getNodes(self,mapdata):#get the nodes
        '''generate nodes'''
        nodes = []  #list of nodes
        x = 0#x position of the node
        y = 0#y position of the node
        id = 0#id of the node
        for row in mapdata:#loop through each row in the map
            nodeRow = []#list of nodes in the row
            for tile in row:#loop through each tile in the row
                if tile !=1:#if the tile is not a node
                    nodeRow.append(None)#add a none to the row
                if tile == 1:#if the tile is a node
                    nodeRow.append(Node(id,x*16+8,y*16))#add a node to the row
                    id +=1#increment the id
                x += 1#increment the x position
            x = 0#reset the x position
            y +=1#increment the y position
            nodes.append(nodeRow)#add the row to the list of nodes
        #get rid of any nodes we don't need such as nodes that have nodes above them
        for row in nodes:#loop through each row in nodes
            for node in row:#loop through each node in the row
                if node != None:#if the node is not none
                    if self.getRelativeStateOfNode(row.index(node),nodes.index(row),0,-1,nodes) != None:#if the node above the current node is not none
                        row[row.index(node)] = None#set the node to none
        '''generate connections'''
        amountOfRowsOfNodes = len(nodes)#get the amount of rows in nodes
        for rowIndex in range(0, amountOfRowsOfNodes):#loop through each row in nodes
            row = nodes[rowIndex]#get the row
            amountOfNodesInRow = len(row)#get the amount of nodes in the row
            for nodeIndex in range(0, amountOfNodesInRow):#loop through each node in the row
                node = row[nodeIndex]#get the node
                if node != None:
                    '''<---make connections on the same y levels:--->'''
                    if (nodeIndex != amountOfNodesInRow-1 and self.getRelativeStateOfNode(nodeIndex,rowIndex,1,0,nodes) != None and self.getRelativeStateOfNode(nodeIndex,rowIndex,0,-1,nodes) is None):#if the node is not the last node in the row and there is a node to the right and there is no node above the node to the right 
                        node.add_connection(row[nodeIndex+1],[1,0])#add a connection to the node to the right
                    if nodeIndex != 0 and self.getRelativeStateOfNode(nodeIndex,rowIndex,-1,0,nodes) != None and self.getRelativeStateOfNode(nodeIndex,rowIndex,0,-1,nodes) is None:#if the node is not the first node in the row and there is a node to the left and there is no node above the node to the left
                        node.add_connection(row[nodeIndex-1],[1,0])#add a connection to the node to the left
                    '''<---make connections on different y levels:--->'''
                    #check if there is a node above the current node by 1 and 2
                    if (self.getRelativeStateOfNode(nodeIndex,rowIndex,0,-1,nodes) is None and#is there no node above by 1
                        self.getRelativeStateOfNode(nodeIndex,rowIndex,0,-2,nodes) is None):#is there no node above by 2
                        #if so look for possible connections to make
                        ConnectionYRange = 7#the range of y values to check for nodes
                        ConnectionXRange = 2#the range of x values to check for nodes
                        for y in range(0,ConnectionYRange):#loop through the y range
                            for x in range(-ConnectionXRange,ConnectionXRange+1):#loop through the x range
                                if abs(x) == 0 or abs(x) == 1:continue
                                possibleConnection = self.getRelativeStateOfNode(nodeIndex,rowIndex,x,y,nodes)#get the node at the current x and y
                                if possibleConnection != None:#if there is a possible connection
                                    #check for nodes that could obstuct the connection:
                                    if ((x > 0 and self.getRelativeStateOfNode(nodeIndex,rowIndex,x,y-1,nodes) is None and self.getRelativeStateOfNode(nodeIndex,rowIndex,1,0,nodes) is None) or 
                                        (x < 0 and self.getRelativeStateOfNode(nodeIndex,rowIndex,-1,0,nodes) is None and self.getRelativeStateOfNode(nodeIndex,rowIndex,x,y-1,nodes) is None)):
                                            #make a connection
                                            node.add_connection(possibleConnection,[x,y])
        
        nodelist = []#list of all nodes
        for row in nodes:#loop through each row in nodes
            for node in row:#loop through each node in the row
                if node != None:#if the node is not none
                    nodelist.append(node)#add the node to the list of nodes
        return nodelist#return the list of nodes
                            
                                    

