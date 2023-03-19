'''
    this scripts is used all types of testing for the game

'''

#------------------testing db------------------
def runSqlStateMent():
    from scripts.dbHandler import DBHandler
    dbH = DBHandler()
    while True:
        print('Enter a sql statement to run:')
        sql = input()
        if sql == 'exit':
            break
        try:
            print(dbH.db.manualSQLCommand(sql))
        except:
            print('Error')

#runSqlStateMent()

#------------------testing db------------------
import unittest
def getNodeIds(listOfNodes):
    ids = []
    for node in listOfNodes:
        ids.append(node['node'].id)
    return ids
class testClass(unittest.TestCase):
    
    def test_NodePlaceMent(self):
        mapData = [[0,0,0,0,0],
                   [0,0,0,0,0],
                   [0,0,1,0,0],
                   [0,0,0,0,0],
                   [0,0,0,0,0],
                   [1,1,1,1,1]
                   ]
        from scripts.graph import Graph
        graph = Graph(mapData)
        nodesList = graph.nodes
        node = {}
        for Anode in nodesList:
            node[Anode.id] = Anode

        adjacencyList = {0: [1,5],
                         1: [0,2],
                         2: [1,3],
                         3: [2,4],
                         4: [3,5],
                         5: [0,4]
                         }
        #node 0:
        x = node[0].x
        y = node[0].y
        connections = getNodeIds(node[0].connections)
        connections.sort()
        assert node[0].x == 40
        assert node[0].y == 32
        assert connections == adjacencyList[0]
        #node 1:
        x = node[1].x
        y = node[1].y
        connections = getNodeIds(node[1].connections)
        connections.sort()
        assert node[1].x == 8
        assert node[1].y == 80
        assert connections == adjacencyList[1]
        #node 2:
        x = node[2].x
        y = node[2].y
        connections = getNodeIds(node[2].connections)
        connections.sort()
        assert node[2].x == 24
        assert node[2].y == 80
        assert connections == adjacencyList[2]
        #node 3:
        x = node[3].x
        y = node[3].y
        connections = getNodeIds(node[3].connections)
        connections.sort()
        assert node[3].x == 40
        assert node[3].y == 80
        assert connections == adjacencyList[3]
        #node 4:
        x = node[4].x
        y = node[4].y
        connections = getNodeIds(node[4].connections)
        connections.sort()
        assert node[4].x == 56
        assert node[4].y == 80
        assert connections == adjacencyList[4]
        #node 5:
        x = node[5].x
        y = node[5].y
        connections = getNodeIds(node[5].connections)
        connections.sort()
        assert node[5].x == 72
        assert node[5].y == 80
        assert connections == adjacencyList[5]
        return nodesList

        
    def test_AStarAlgorithm(self):
        nodesList = self.test_NodePlaceMent()
        from scripts.ai import Ai
        from scripts.node import Node
        #test 1: find path from node 1 to node 3, 1->2->3 
        path = Ai.findPath(nodesList[1],nodesList[3])
        idpath = []
        for node in path:
            idpath.append(node.id)
        assert idpath == [1,2,3]
        #test 2: find path from node 1 to node 4, 1->2->3->4
        path = Ai.findPath(nodesList[1],nodesList[4])
        idpath = []
        for node in path:
            idpath.append(node.id)
        assert idpath == [1,2,3,4]
        #test 3: find path from node 5 to node 0, 5->0 
        path = Ai.findPath(nodesList[5],nodesList[0])
        idpath = []
        for node in path:
            idpath.append(node.id)
        assert idpath == [5,0]
        #test 4: find path from node 3 to node 0, 3->2->1->0
        path = Ai.findPath(nodesList[3],nodesList[0])
        idpath = []
        for node in path:
            idpath.append(node.id)
        assert idpath == [3,2,1,0]
        
if __name__ == '__main__':
    unittest.main()