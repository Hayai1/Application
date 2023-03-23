from queue import PriorityQueue
class Ai:
    def __init__(self,rect,target,graph) -> None:
        self.left = False#is the ai moving left
        self.right = False#is the ai moving right
        self.graph = graph#the ai's graph
        self.distanceBetweenNodes = 0#the distance between the ai's nodes
        self.path = None#the ai's path
        self.nextNode = None#the ai's next node to move to 
        self.moving = False#is the ai moving
        self.jumping = False#is the ai jumping
        self.nodePointer = 0#the ai's node pointer
        self.frame = 0#the ai's frame
        self.movingFrames = 0#the ai's moving frames
        self.newPathTimer = 0#the ai's new path timer
        self.rect = rect#the ai's rect
        self.target = target#the ai's target
        self.currentNode = self.graph.getNodeCloseTo(rect)#the node currently on
    @staticmethod
    def findPath(start,goal):
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
                    closedList.append(q)#add q to the closed list
                    path = []#the path
                    path.append(closedList[0])#add the starting node to the path
                    for i in range(1,len(closedList)):#for each node in the closed list
                        connections = []#the connections
                        for connection in path[-1].connections:#for each connection in the last node in the path
                            connections.append(connection['node'])#add the node to the connections
                        if closedList[i] in connections:#if the node in the closed list is in the connections
                            path.append(closedList[i])#add the node to the path
                    path.append(goal)#add the goal to the path
                    return path#return the path
                else:
                    #else, compute both g and h for successor
                    successor.setCosts(g=gScores[successors.index(successor)],end=goal,parent=q)#set the costs
                for node in openList.queue:#for each node in the open list
                    if node.id == successor.id and node.f <= successor.f:#if the node in the open list has a lower f than the successor
                        skipSuccessor = True#skip the successor
                        break#break the loop
                if skipSuccessor:#if the successor is to be skipped
                    skipSuccessor = False#set skip successor to false
                    continue#return to the start of the loop
                for node in closedList:#for each node in the closed list
                    if node.id == successor.id and node.f <= successor.f:#if the node in the closed list has a lower f than the successor
                        skipSuccessor = True#skip the successor
                        break#break the loop
                if skipSuccessor:#if the successor is to be skipped
                    skipSuccessor = False#set skip successor to false
                    continue#return to the start of the loop
                openList.put(successor)#add the successor to the open list
            closedList.append(q)#add q to the closed list

    def getDirection(self,airTimer):
        left = None#is the ai moving left
        right = None#is the ai moving right
        jump = False#is the ai jumping
        self.newPathTimer +=1#increment the new path timer
        #-------------------------------------------------------------#
        #check if a current path exists
        if self.movingFrames == self.frame:#if the ai has finished moving to the next node
            self.moving = False#set moving to false

        if self.movingFrames < self.frame:#error can occur here
            self.path = None#set the path to none
            self.nodePointer = 0#set the node pointer to 0
            self.nextNode = None#set the next node to none
            self.frame = 0#set the frame to 0

        if self.jumping:#if the ai is jumping
            if self.nextNode is not None and self.nextNode.y > self.rect.y:#if the next node is above the ai
                self.jumping = False#set jumping to false
                if self.nextNode.x > self.currentNode.x:#if the next node is to the right of the ai
                    left = False#set left to false
                    right = True#set right to true
                elif self.nextNode.x < self.currentNode.x:#if the next node is to the left of the ai
                    right = False#set right to false
                    left = True#set left to true
                self.movingFrames = abs(self.currentNode.getG(self.nextNode)[0]*8)#set the moving frames to the distance between the current node and the next node
                self.frame = 0#set the frame to 0

        if self.path == None:#if the path is none
            #check if player is in aggro range
            if self.getAggro():
                #if player is in aggro range then get a path to the player
                self.newPathTimer = 0
                self.path = self.findPath(self.graph.getNodeCloseTo(self.rect),self.graph.getNodeCloseTo(self.target.rect))   
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
            
    def getPath(self,currentLocation,player):
        target = self.graph.getNodeCloseTo(player)
        path = self.findPath(currentLocation,target)
        #self.drawPath(target,path)
        return path

    def drawPath(self,target,path):#draw the path (used for testing)

        for nodes in self.graph.nodes:#for each node in the graph
            nodes.color = (255,255,0)#set the color to yellow
        target.color = (0,255,0)#set the target color to green
        if path is not None:#if the path is not none
            for node in path:#for each node in the path
                node.color = (0,0,255)#set the color to blue
    def getAggro(self):#check if the player is in aggro range
        if self.rect.x - self.target.x < 300 and self.rect.x - self.target.x > -300 and self.rect.y - self.target.y < 300 and self.rect.y - self.target.y > -300:#if the player is in aggro range
            return True#return true
        return False#return false
    def update(self,airTimer):#update the ai
        left,right,jump = self.getDirection(airTimer)#get the direction to move in
        return left,right,jump#return the direction to move in