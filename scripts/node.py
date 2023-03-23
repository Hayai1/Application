import math
class Node:
    def __init__(self,id,x,y):#id is the id of the node, x and y are the coordinates of the node
        self.id = id#id of the node
        self.pos = [x,y]#position of the node
        self.x = x#x coordinate of the node
        self.y = y#y coordinate of the node
        self.color = (255,255,0)#color of the node
        self.connections = []#connections of the node
        self.g = 0#cost of the node
        self.h = 0#heuristic of the node
        self.f = 0#f of the node
        
    def setCosts(self,g=None,end=None):#sets the costs of the node
        if end is not None:#if the end node is not none
            self.h = math.sqrt((self.x - end.x)**2 + (self.y - end.y)**2)#set the heuristic to the distance between the node and the end node
        if g is not None:#if the g is not none
            self.g = g#set the g to the g
        self.f = self.g[0] + self.g[1] + self.h#set the f to the g plus the h
    def __eq__(self, other):#if the node is equal to another node
        if other is None: #if the other node is none
            return False#return false
        return self.id == other.id#return if the id of the node is equal to the id of the other node

    def __lt__(self, other):#if the node is less than another node used for when the node is put into the priority queue
        return (self.f < other.f)#return if the f of the node is less than the f of the other node
    
    def _gt__(self, other):#if the node is greater than another node used for when the node is put into the priority queue
        return (self.f > other.f)#return if the f of the node is greater than the f of the other node
    def add_connection(self,node,g):#adds a connection to the node
        flag = True#flag for if the connection is already in the connections list
        for connection in self.connections:#for each connection in the connections list
            if connection['node'].id == node.id:#if the id of the node in the connection is equal to the id of the node
                flag = False#set the flag to false
        if flag:#if the flag is true
            self.connections.append({'node' : node,'g' : g})#add the connection to the connections list
        flag = True#set the flag to true
        for connection in node.connections:#for each connection in the connections list of the node
            if connection['node'].id == self.id:#if the id of the node in the connection is equal to the id of the node
                flag = False#set the flag to false
        if flag:#if the flag is true
            node.connections.append({'node' : self,'g' : g})#add the connection to the connections list of the node
    def getG(self,node):#gets the g of the connection to the node
        for connection in self.connections:#for each connection in the connections list
            if connection['node'] == node:#if the node in the connection is equal to the node
                return connection['g']#return the g of the connection
        







