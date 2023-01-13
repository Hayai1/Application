from queue import PriorityQueue
class Ai:
    def __init__(self,graph) -> None:
        self.graph = graph
        self.distanceBetweenNodes = 0

    def findPath(self,start,goal):
        #init the open list
        openList = PriorityQueue()#queue
        #init the closed list
        closedList = []
        #put the starting node on the open list
        openList.put(start)
        skipSuccessor = False
        #while the open list is not empty
        while not openList.empty():
            #find the node with the least f on the open list, call it "q" and pop q off the open list
            q = openList.get()
            #generate q's successors and set their parents to q
            successors = []
            gScores = []
            for connection in q.connections:
                successors.append(connection['node'])
                gScores.append(connection['g'])
            for successor in successors:
                #if successor is the goal, stop the search
                if successor.id == goal.id:
                    closedList.append(q)
                    path = []
                    path.append(closedList[0])
                    for i in range(1,len(closedList)):
                        connections = []
                        for connection in path[-1].connections:
                            connections.append(connection['node'])
                        if closedList[i] in connections:
                            path.append(closedList[i])
                    return path
                else:
                    #else, compute both g and h for successor
                    successor.setCosts(g=gScores[successors.index(successor)],end=goal,parent=q)
                for node in openList.queue:
                    if node.id == successor.id and node.f <= successor.f:
                        skipSuccessor = True
                        break
                if skipSuccessor:
                    skipSuccessor = False
                    continue
                for node in closedList:
                    if node.id == successor.id and node.f <= successor.f:
                        skipSuccessor = True
                        break
                if skipSuccessor:
                    skipSuccessor = False
                    continue
                openList.put(successor)
            closedList.append(q)

    def FindAndDrawPath(self,currentLocation,player):
        for nodes in self.graph.nodes:
            nodes.color = (255,255,0)
        target = self.graph.getNodeCloseTo(player)
        path = self.findPath(currentLocation,target)
        target.color = (0,255,0)
        if path is not None:
            for node in path:
                node.color = (0,0,255)
        return path