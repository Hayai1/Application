import math
class Node:
    def __init__(self,id,x,y):
        self.id = id
        self.pos = [x,y]
        self.x = x
        self.y = y
        self.color = (255,255,0)
        self.connections = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        
    def setCosts(self,g=None,end=None,parent=None):
        if parent is not None:
            self.parent = parent
        if end is not None:
            self.h = math.sqrt((self.x - end.x)**2 + (self.y - end.y)**2)
        if g is not None:
            self.g = g
        self.f = self.g[0] + self.g[1] + self.h
    def __eq__(self, other):
        if other is None: 
            return False
        return self.id == other.id

    def __lt__(self, other):
        return (self.f < other.f)
    
    def _gt__(self, other):
        return (self.f > other.f)
    def add_connection(self,node,g):
        flag = True
        for connection in self.connections:
            if connection['node'].id == node.id:
                flag = False
        if flag:
            self.connections.append({'node' : node,'g' : g})
        flag = True
        for connection in node.connections:
            if connection['node'].id == self.id:
                flag = False
        if flag:
            node.connections.append({'node' : self,'g' : g})
    def getG(self,node):
        for connection in self.connections:
            if connection['node'] == node:
                return connection['g']
        







