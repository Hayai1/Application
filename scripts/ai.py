from queue import PriorityQueue
class Ai:
    def __init__(self,rect,target,graph) -> None:
        self.left = False
        self.right = False
        self.graph = graph
        self.distanceBetweenNodes = 0
        self.path = None
        self.nextNode = None   
        self.moving = False
        self.jumping = False
        self.nodePointer = 0
        self.frame = 0
        self.movingFrames = 0
        self.newPathTimer = 0
        self.rect = rect
        self.target = target
        self.currentNode = self.graph.getNodeCloseTo(rect)

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

    def getDirection(self,airTimer):
        left = None
        right = None
        jump = False
        self.newPathTimer +=1
        #-------------------------------------------------------------#
        #check if a current path exists
        if self.movingFrames == self.frame:
            self.moving = False

        if self.movingFrames < self.frame:#error can occur here
            self.path = None
            self.nodePointer = 0
            self.nextNode = None
            self.frame = 0

        if self.jumping:
            if self.nextNode is not None and self.nextNode.y > self.rect.y:
                self.jumping = False
                if self.nextNode.x > self.currentNode.x:
                    left = False
                    right = True
                elif self.nextNode.x < self.currentNode.x:
                    right = False
                    left = True
                self.movingFrames = abs(self.currentNode.getG(self.nextNode)[0]*8)
                self.frame = 0

        if self.path == None:
            #check if player is in aggro range
            if self.getAggro():
                #if player is in aggro range then get a path to the player
                self.newPathTimer = 0
                self.path = self.FindAndDrawPath(self.graph.getNodeCloseTo(self.rect),self.target)   
            #check if currently in the process from moving to the next node
        else:
            if not self.moving:
                #get the actual node in terms of postion in the graph
                closestNode = self.graph.getNodeCloseTo(self.rect)
                #if the actual node is not the same as the current node then set the path to none and move on
                if self.nodePointer != 0 and closestNode != self.nextNode and airTimer < 4:
                    self.path = None
                    self.nodePointer = 0
                    self.nextNode = None
                else:#if the actual node is the same as the current node then get the next node to move to
                    if self.nextNode is None:
                        self.currentNode = self.path[0]
                    else:
                        self.currentNode = self.nextNode
                    left = False
                    right = False
                    self.nodePointer += 1
                    if self.nodePointer <= len(self.path) - 1:
                        self.nextNode = self.path[self.nodePointer]
                        #using the current node connection to the next node g score to get the next node
                        gScore = self.currentNode.getG(self.nextNode)
                        gScoreX = gScore[0]
                        gScoreY = gScore[1]
                        #state which directions to move in and if jumping is needed
                        if gScoreY != 0 and self.currentNode.y > self.nextNode.y:
                            jump = True
                            self.jumping = True
                            self.movingFrames = 0
                        elif self.nextNode.x > self.currentNode.x:
                            left = False
                            right = True
                            self.movingFrames = abs(gScoreX*8)
                        elif self.nextNode.x < self.currentNode.x:
                            right = False
                            left = True
                            self.movingFrames = abs(gScoreX*8)
                        #reset the frame
                        self.frame = 1
                        self.moving = True#state that the enemy is moving
                    else:
                        self.path = None
                        self.nodePointer = 0
                        self.nextNode = None
            else:#if the enemy is moving then move
                self.frame += 1
        return left,right,jump
            
    def FindAndDrawPath(self,currentLocation,player):
        target = self.graph.getNodeCloseTo(player)
        path = self.findPath(currentLocation,target)
        #self.drawPath(target,path)
        return path

    def drawPath(self,target,path):

        for nodes in self.graph.nodes:
            nodes.color = (255,255,0)
        target.color = (0,255,0)
        if path is not None:
            for node in path:
                node.color = (0,0,255)
    def getAggro(self):
        if self.rect.x - self.target.x < 300 and self.rect.x - self.target.x > -300 and self.rect.y - self.target.y < 300 and self.rect.y - self.target.y > -300:
            return True
        return False
    def update(self,airTimer):
        left,right,jump = self.getDirection(airTimer)
        return left,right,jump