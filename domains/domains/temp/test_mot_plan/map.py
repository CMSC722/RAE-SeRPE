

class map:
    rooms=[]
    doors={}
    observMatrix={}
    adjacencyMatrix={}


    def __init__(self):
        self.defDoors()
        self.defObservMatrix()
        self.defRooms()
        self.defAdjacencyMatrix()

    def defRooms(self):
        self.rooms=['A','B','C','D','E','F']

    def defDoors(self):
        self.doors={
            'Door A':['A','G'],
            'Door B': ['B','H'],
            'Door C': ['C','I'],
            'Door D': ['D','J'],
            'Door E': ['E','K'],
            'Door F': ['F','L']
        }

    # def defDoors(self):
    #     self.doors={
    #         'A': 'Door A',
    #         'B': 'Door B',
    #         'C': 'Door C',
    #         'D': 'Door D',
    #         'E': 'Door E',
    #         'F': 'Door F',
    #     }

    def defObservMatrix(self):
        self.observMatrix={
            'A':set(['A','G']),
            'B':set(['B','H']),
            'C':set(['C','I']),
            'D':set(['D','J','K','L']),
            'E':set(['E','K']),
            'F':set(['F','L']),
            'G':set(['A','G','H']),
            'H':set(['B','H','G','I','J']),
            'I':set(['C','H','I','J']),
            'J':set(['D','J','H','I','K','L']),
            'K':set(['E','L','J','K']),
            'L':set(['F','K','J','L'])
        }

    def defAdjacencyMatrix(self):
        self.adjacencyMatrix={
            'A': [1,0,0,0,0,0,1,0,0,0,0,0],
            'B': [0,1,0,0,0,0,0,1,0,0,0,0],
            'C': [0,0,1,0,0,0,0,0,1,0,0,0],
            'D': [0,0,0,1,0,0,0,0,0,1,1,1],
            'E': [0,0,0,0,1,0,0,0,0,0,1,0],
            'F': [0,0,0,0,0,1,0,0,0,0,0,1],
            'G': [1,0,0,0,0,0,1,1,0,0,0,0],
            'H': [0,1,0,0,0,0,1,1,1,1,0,0],
            'I': [0,0,1,0,0,0,0,1,1,1,0,0],
            'J': [0,0,0,1,0,0,0,1,1,1,1,1],
            'K': [0,0,0,0,1,0,0,0,0,1,1,1],
            'L': [0,0,0,0,0,1,0,0,0,1,1,1]

        }

    def observeable(self,location1,location2):
        if location1 in self.observMatrix[location2]:
            return True
        else:
            return False

