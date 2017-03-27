

class map:
    rooms=[]
    doors={}
    observMatrix={}


    def init(self):
        self.defDoors()
        self.defObservMatrix()
        self.defRooms()

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

    def defDoors(self):
        self.doors={
            'A':'Door A',
            'B': 'Door B',
            'C': 'Door C',
            'D': 'Door D',
            'E': 'Door E',
            'F': 'Door F',
        }

    def defObservMatrix(self):
        self.observMatrix={
            'A':['A','G'],
            'B':['B','H'],
            'C':['C','I'],
            'D':['D','J','K','L'],
            'E':['E','K'],
            'F':['F','L'],
            'G':['A','G','H'],
            'H':['B','H','G','I','J'],
            'I':['C','H','I','J'],
            'J':['D','J','H','I','K','L'],
            'K':['E','L','J','K'],
            'L':['F','K','J','L']
        }


    def observeable(self,location1,location2):
        if location1 in self.observMatrix[location2]:
            return True
        else:
            return False

    # def naivePath(self,location1, location2):






