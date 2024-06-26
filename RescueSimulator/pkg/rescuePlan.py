from localBeamSearch import LocalBeamSearch
from state import State

class RescuePlan:
    dictDir = {
        'N':State(-1,0),
        'S':State(1,0),
        'L':State(0,1),
        'O':State(0,-1),
        'NO':State(-1,-1),
        'NE':State(-1,1),
        'SO':State(1,-1),
        'SE':State(1,1)
    }

    def __init__(self,model,initialState,stateMesh,prob):

        self.initialState = initialState
        self.currentState = initialState

        self.prob = prob

        #Tempo estimado para volta
        self.estTime = 0

        self.path = []
        
        self.localSearch = LocalBeamSearch(model,initialState,prob,stateMesh)
    
    def calcPath(self,ts,victims):
        if(self.localSearch.calcMinVictimsDist(victims) == -1):
            return -1
        numNei = int(len(victims)/10)+1
        numSwaps = int(len(victims)/10)+1
        self.path = self.localSearch.localSearch(ts,20,numNei,200,numSwaps)
        return 1
    def chooseAction(self):
        if len(self.path) == 0:
            return 'nop',self.currentState
        action = self.path[0]
        state = self.currentState + self.dictDir[action]
        self.path.pop(0)

        return action,state


