from copy import deepcopy
from random import randint
from state import State
import math
class StraightPathPlan:

    #Classe auxiliar que mantém as adjacências entre as posições exploradas (mantém as ações possíveis para cada posição).
    class Node:
        revDir = {
            'N':'S',
            'S': 'N',
            'L': 'O',
            'O': 'L',
            'NE': 'SO',
            'SO': 'NE',
            'NO': 'SE',
            'SE': 'NO',
        }
        def __init__(self,state):
            #Vizinhos conhecidos de cada posição.
            self.neighbors = {}
            #Posição de cada nó.
            self.state = state

        def add_neighbor(self,node,dir):
            self.neighbors[dir] = node
            #Adiciona no nó vizinho este nó. Porém, se o vizinho está a Leste, o vizinho adiciona este nó a Oeste.
            node.neighbors[self.revDir[dir]] = self

    #Classe auxiliar para manter os estados explorados no algoritmo A*.
    class AStarState:
        def __init__(self,node):
            #Encadeia os estados para a construção da solução.
            self.parent = None
            #Nó que o estado representa.
            self.node = node
            #Atributo auxiliar que mantém o custo até este nó durante a execução do A*.
            self.cost = 0.0
            #Direção do nó pai para este nó.
            self.dir = ''
            #States até este nó. Serve para evitar com que nó já visitados sejam incluidos novamente.
            self.path = []
            #APAGARR!!!!!
            self.heur = 0

            
    dictCost = {
        'N':1,
        'S':1,
        'L':1,
        'O':1,
        'NO':1.5,
        'NE':1.5,
        'SO':1.5,
        'SE':1.5
    }
    dictDir = {
        'N':(-1,0),
        'S':(1,0),
        'L':(0,1),
        'O':(0,-1),
        'NO':(-1,-1),
        'NE':(-1,1),
        'SO':(1,-1),
        'SE':(1,1)
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

        #Tempo estimado para volta
        self.estTime = 0

        #Define o estado atual do agente: procurando (0) ou voltando para a base (1)
        self.state = 0

        #Define o caminho de volta
        self.path = []

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
        self.currentState = state
        self.upGraph()
        self.upShortestWayBack()
    
    def updateTimeLeft(self,time):
        if(time-1<self.estTime):
            self.state = 1

    #Função para atualizar as adjacências entre os nós (posições) conhecidos.
    def upGraph(self):
        posDir = self.posDirections(self.currentState)
        #Se não foi criado um nó para a posição atual:
        if (self.currentState.row,self.currentState.col) not in self.dictNode:
            self.dictNode[(self.currentState.row,self.currentState.col)] = self.Node(self.currentState)
        curNode = self.dictNode[(self.currentState.row,self.currentState.col)]
        for dir in posDir:
            curNode.add_neighbor(self.dictNode[dir[1]],dir[0])

    def upShortestWayBack(self):
        self.a_star_algorithm()

    #Calcula o melhor caminho para voltar.    
    def a_star_algorithm(self):

        #Estimativas de cada estado que estão na borda (State:estimativa)
        est = {}
        #goal = self.initialState
        goal = self.currentState
        curNode = self.dictNode[(self.initialState.row,self.initialState.col)]

        #Cria um estado inicial para o algoritmo A*.
        curState = self.AStarState(curNode)

        minPathNode = {}
        nodeDict = {}
        borderNodes = {}

        minPathNode[curNode] = 0

        for dir,node in curNode.neighbors.items():
            heur = self.calcHeuristic(node.state,goal)
            cost = self.dictCost[dir]

            newState = self.AStarState(node)
            newState.parent = curState
            newState.cost = cost
            newState.dir = self.Node.revDir[dir]
            newState.path.append(curNode.state)
            est[newState] = heur+cost

            minPathNode[node] = cost
            nodeDict[newState] = node
            borderNodes[newState] = node
        if len(est) == 0:
            return

        #Pega o estado com a menor estimativa na borda.
        curState =  min(est, key=est.get)
        curNode = curState.node
        
        del est[curState]

        while(curNode.state!=goal):
            for dir,node in curNode.neighbors.items():
                #Se o estado já foi descoberto nesse ramo (evita loops).
                if node.state not in curState.path:
                    heur = self.calcHeuristic(node.state,goal)

                    newState = self.AStarState(node)
                    newState.parent = curState
                    newState.cost = self.dictCost[dir]+curState.cost
                    newState.heur=heur
                    newState.dir = self.Node.revDir[dir]
                    #Cada estado mantém o caminho até ele
                    newState.path = deepcopy(curState.path)
                    newState.path.append(curNode.state)
                 
                    if node in minPathNode.keys():
                        if newState.cost>minPathNode[node]:
                            continue
                        else:
                            if node in borderNodes.values():
                                state = list(borderNodes.keys())[list(borderNodes.values()).index(node)]
                                del borderNodes[state]
                                del est[state]
                                 
                    est[newState] = heur+newState.cost
                    borderNodes[newState] = node
                    minPathNode[node] = newState.cost
                    '''
                    if(goal == State(18,20)):
                        print(f'Nó a ser expandido, Heuristica:{newState.heur}, Estimativa:{newState.heur+newState.cost}')
                        
                        maze = [['.' for i in range(26)] for j in range(26)]
                        maze[goal.row][goal.col] = 'A'
                        maze[node.state.row][node.state.col] = 'X'
                        for i in newState.path:
                            maze[i.row][i.col] = 'X'
                        for i in range(20):
                            col = ""
                            for j in range(25):
                                col += f'{maze[i][j]} '
                            col += str(i)
                            print(col)
                        e = ''
                        for i in est.values():
                            e+= str(i)+ ' '
                        print(e)
                '''
            curState =  min(est, key=est.get)
            curNode = curState.node

            del est[curState]
            del borderNodes[curState]

        self.estTime = curState.cost
        self.path.clear()

        while curState!=None:
            self.path.append(curState.dir)
            curState = curState.parent
        
    def calcHeuristic(self,state1,state2):
        difR = abs(state1.row-state2.row)
        difC = abs(state1.col-state2.col)
        if(difR>difC):
            return 1.5*(difC) + (difR-difC) 
        else:
            return 1.5*(difR) + (difC-difR) 

    #Direções que o agente pode ir de acordo com a sua crença do mapa.
    def posDirections(self,state):
        posDir = []
        if self.prob.mazeBelief[state.row][state.col] == 1:
            posDir.append(('NO',(state.row-1,state.col-1)))
        if self.prob.mazeBelief[state.row][state.col+1] == 1:
            posDir.append(('N',(state.row-1,state.col)))
        if self.prob.mazeBelief[state.row][state.col+2] == 1:
            posDir.append(('NE',(state.row-1,state.col+1)))
        if self.prob.mazeBelief[state.row+1][state.col+2] == 1:
            posDir.append(('L',(state.row,state.col+1)))
        if self.prob.mazeBelief[state.row+2][state.col+2] == 1:
            posDir.append(('SE',(state.row+1,state.col+1)))
        if self.prob.mazeBelief[state.row+2][state.col+1] == 1:
            posDir.append(('S',(state.row+1,state.col)))
        if self.prob.mazeBelief[state.row+2][state.col] == 1:
            posDir.append(('SO',(state.row+1,state.col-1)))
        if self.prob.mazeBelief[state.row+1][state.col] == 1:
            posDir.append(('O',(state.row,state.col-1)))
        return posDir

    def chooseAction(self):
        if(self.state == 0):
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
        else:
            action = self.path[0]
            state = State(self.currentState.row+self.dictDir[action][0],self.currentState.col+self.dictDir[action][1])
            self.path.pop(0)
            return action,state
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


        
       
        
        
