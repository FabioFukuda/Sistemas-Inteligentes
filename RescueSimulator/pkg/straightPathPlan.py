from copy import deepcopy
from random import randint
from state import State
import math
class StraightPathPlan:

    class Node:
        revDir = {
            'N':'S',
            'S': 'N',
            'L': 'O',
            'O': 'L',
            'NL': 'SO',
            'SO': 'NL',
            'NO': 'SL',
            'SL': 'NO',
        }
        def __init__(self,state):
            self.neighbors = {}
            self.state = state

        def add_neighbor(self,node,dir):
            self.neighbors[dir] = node
            node.neighbors[self.revDir[dir]] = self

    class AStarState:
        def __init__(self,node):
            self.parent = None
            self.node = node
            self.visited = False
            self.cost = 0
            self.dir = ''
            self.path = []

    dictCost = {
        'N':1,
        'S':1,
        'L':1,
        'O':1,
        'NO':1.5,
        'NL':1.5,
        'SO':1.5,
        'SL':1.5
    }

    def __init__(self, initialState, name = "none", mesh = "square",prob = None):

        self.walls = []
        self.initialState = initialState
        self.currentState = initialState
        self.actions = []

        self.nextAction = 'O'
        self.EastDir = True
        self.SouthDir = False
        self.prob = prob

        #Guarda o caminho de volta.
        self.wayBack = None
        #Dict para acessar os nós (chave -> posição no mapa)
        self.dictNode = {}
        self.dictNode[(0,0)] = self.Node(self.currentState)

    def setWalls(self, walls):
        row = 0
        col = 0
        for i in walls:
            col = 0
            for j in i:
                if j == 1:
                    self.walls.append((row, col))
                col += 1
            row += 1
        
    def updateCurrentState(self, state):
        if(self.currentState == state):
            self.nextAction = 'S'

        if state == State(5,5):
            print('PARAAAA')

        self.currentState = state
        self.upGraph()
        self.upShortestWayBack()
    
        
    
    def upGraph(self):
        posDir = self.posDirections(self.currentState)
        if (self.currentState.row,self.currentState.col) not in self.dictNode:
            self.dictNode[(self.currentState.row,self.currentState.col)] = self.Node(self.currentState)
        curNode = self.dictNode[(self.currentState.row,self.currentState.col)]
        for dir in posDir:
            curNode.add_neighbor(self.dictNode[dir[1]],dir[0])

    def upShortestWayBack(self):
        self.a_star_algorithm()

    #Calcula o melhor caminho para voltar.    
    def a_star_algorithm(self):

        #Estimativas de cada estado que estão na borda
        est = {}
        goal = self.initialState

        curNode = self.dictNode[(self.currentState.row,self.currentState.col)]
        curState = self.AStarState(curNode)

        for dir,node in curNode.neighbors.items():
            heur = self.calcHeuristic(node.state)
            cost = self.dictCost[dir]

            newState = self.AStarState(node)
            newState.parent = curState
            newState.cost = cost
            newState.dir = self.Node.revDir[dir]
            newState.path.append(curNode.state)

            est[newState] = heur+cost

            
        if len(est) == 0:
            return

        curState =  min(est, key=est.get)
        curNode = curState.node
        del est[curState]

        while(curNode.state!=goal):
            for dir,node in curNode.neighbors.items():
                if node.state not in curState.path:
                    heur = self.calcHeuristic(node.state)
                    newState = self.AStarState(node)
                    newState.parent = curState
                    newState.cost = cost+curState.cost
                    newState.dir = self.Node.revDir[dir]
                    newState.path = deepcopy(curState.path)
                    newState.path.append(node.state)
                    est[newState] = heur+cost

            curState =  min(est, key=est.get)
            curNode = curState.node
            del est[curState]
        path = ''
        while curState!=None:
            path += curState.dir + ' '
            curState = curState.parent
        print('Caminho encontrado: ' + path)
    def calcHeuristic(self,state):
        return math.sqrt(math.pow((state.row-self.initialState.row),2)+math.pow((state.col-self.initialState.col),2))

    #Direções que o agente pode ir de acordo com a sua crença do mapa.
    def posDirections(self,state):
        posDir = []
        if self.prob.mazeBelief[state.row][state.col] == 1:
            posDir.append(('NO',(state.row-1,state.col-1)))
        if self.prob.mazeBelief[state.row][state.col+1] == 1:
            posDir.append(('N',(state.row-1,state.col)))
        if self.prob.mazeBelief[state.row][state.col+2] == 1:
            posDir.append(('NL',(state.row-1,state.col+1)))
        if self.prob.mazeBelief[state.row+1][state.col+2] == 1:
            posDir.append(('L',(state.row,state.col+1)))
        if self.prob.mazeBelief[state.row+2][state.col+2] == 1:
            posDir.append(('SL',(state.row+1,state.col+1)))
        if self.prob.mazeBelief[state.row+2][state.col+1] == 1:
            posDir.append(('S',(state.row+1,state.col)))
        if self.prob.mazeBelief[state.row+2][state.col] == 1:
            posDir.append(('SO',(state.row+1,state.col-1)))
        if self.prob.mazeBelief[state.row+1][state.col] == 1:
            posDir.append(('O',(state.row,state.col-1)))
        return posDir

    def chooseAction(self):
        action = "L"  if self.EastDir == 1 else "O"
   
        if(self.nextAction == 'S'):
            action = self.nextAction
            self.EastDir *= -1
            self.nextAction = "L"  if self.EastDir == 1 else "O"

        match action:
            case 'L':
                return action,State(self.currentState.row,self.currentState.col+1) 
            case 'S':
                return action,State(self.currentState.row+1,self.currentState.col) 
            case 'O':
                return action,State(self.currentState.row,self.currentState.col-1)
    
    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   


#Fonte: https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict
from collections.abc import MutableMapping
class TransformedDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        if type(key) == tuple:
            return self.store[self._keytransform(key)]
        elif type(key) == StraightPathPlan.Node:
            return self.sotre[(key.state.row,key.state.col)]

    def __setitem__(self, key, value):
        self.store[self._keytransform(key)] = value

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)
    
    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return key     


        
       
        
        
