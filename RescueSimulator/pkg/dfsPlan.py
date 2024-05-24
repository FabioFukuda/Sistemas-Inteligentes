from random import randint
from state import State
from aStar import AStar
from dfs import DFS

class DFSPlan:
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
    def __init__(self, initialState:State,stateMesh, name = "none" ,prob = None):

        self.walls = []
        self.initialState = initialState
        self.currentState = initialState
        self.successful = True
        self.prevAction = ''
        self.actions = []

        self.nextAction = 'O'
        self.EastDir = True
        self.SouthDir = False
        self.prob = prob

        #Guarda o caminho de volta.
        self.wayBack = None

        #Tempo estimado para volta
        self.estTime = 0

        #Define o estado atual do agente: procurando (0) ou voltando para a base (1)
        self.state = 0

        #Define o caminho de volta
        self.path = []

        self.dfsPath = []

        self.stateMesh = stateMesh
        self.stateMesh.addNode(self.currentState)
        self.aStar = AStar()
        self.dfs = DFS((initialState.row,initialState.col),prob,stateMesh)

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
            self.successful = False
        else:
            self.successful = True

        self.prevState = self.currentState
        self.currentState = state

        self.upGraph()
        if self.state == 0:
            self.upShortestWayBack()
        
    
    def updateTimeLeft(self,time):
        ''' Verifica se dá tempo para o angente dar mais um passo. A condição time<=self.estTime+1.5 se justifica pois se o agente for
        dar mais um passo, no pior caso o tempo estimado aumenta em 1.5 segundos.'''
        if(time<=self.estTime+5):
            self.state = 1
        return self.state

    #Função para atualizar as adjacências entre os nós (posições) conhecidos.
    def upGraph(self):
        #Virifica todos os vizinhos já explorados do estado atual.
        posDir = self.posDirections(self.currentState)
        #Se não foi criado um nó para a posição atual:
        if (self.currentState.row,self.currentState.col) not in self.stateMesh:
            self.stateMesh.addNode(self.currentState)
        #Adiciona os vizinhos no nó
        self.stateMesh.addNodeNeighbours(self.stateMesh.getNode((self.currentState.row,self.currentState.col)),posDir)

    def upShortestWayBack(self):
        if(self.state == 0):
            self.path.clear()
            self.path ,self.estTime = self.aStar.a_star_algorithm((self.currentState.row,self.currentState.col),
            (self.initialState.row,self.initialState.col),self.stateMesh)

    def validState(self,state):
        return state.col>=0 and state.row>0==0
    #Direções que o agente pode ir de acordo com a sua crença do mapa.
    def posDirections(self,state):
        
        posDir = []
        if self.prob.mazeBelief[state.row][state.col] == 1 and self.prob.mazeBelief[state.row][state.col+1]==1 and self.prob.mazeBelief[state.row+1][state.col]==1 :
            posDir.append(('NO',(state.row-1,state.col-1))) 
        elif self.prevAction=='SE' and self.successful and self.prob.mazeBelief[state.row][state.col] == 1:
            posDir.append(('NO',(state.row-1,state.col-1)))
        if self.prob.mazeBelief[state.row][state.col+1] == 1:
            posDir.append(('N',(state.row-1,state.col)))
        if self.prob.mazeBelief[state.row][state.col+2] == 1 and self.prob.mazeBelief[state.row][state.col+1]==1 and self.prob.mazeBelief[state.row+1][state.col+2]==1:
            posDir.append(('NE',(state.row-1,state.col+1)))
        elif self.prevAction=='SO' and self.successful and self.prob.mazeBelief[state.row][state.col+2] == 1:
            posDir.append(('NE',(state.row-1,state.col+1)))
        if self.prob.mazeBelief[state.row+1][state.col+2] == 1:
            posDir.append(('L',(state.row,state.col+1)))
        if self.prob.mazeBelief[state.row+2][state.col+2] == 1 and self.prob.mazeBelief[state.row+1][state.col+2]==1 and self.prob.mazeBelief[state.row+2][state.col+1]==1:
            posDir.append(('SE',(state.row+1,state.col+1))) 
        elif self.prevAction=='NO' and self.successful and self.prob.mazeBelief[state.row+2][state.col+2] == 1:
            posDir.append(('SE',(state.row+1,state.col+1)))
        if self.prob.mazeBelief[state.row+2][state.col+1] == 1:
            posDir.append(('S',(state.row+1,state.col)))
        if self.prob.mazeBelief[state.row+2][state.col] == 1  and self.prob.mazeBelief[state.row+1][state.col]==1 and self.prob.mazeBelief[state.row+2][state.col+1]==1 :
            posDir.append(('SO',(state.row+1,state.col-1)))
        elif self.prevAction=='NE' and self.successful and self.prob.mazeBelief[state.row+2][state.col] == 1:
            posDir.append(('SO',(state.row+1,state.col-1)))
        if self.prob.mazeBelief[state.row+1][state.col] == 1:
            posDir.append(('O',(state.row,state.col-1)))
        return posDir

    def chooseAction(self):
        
        if(self.state == 0):
            if(len(self.dfsPath) == 0):
                self.dfsPath = self.dfs.dfs((self.currentState.row,self.currentState.col)) 
                if self.dfsPath == 'nop': 
                    self.state=1
                    action = self.path[0]
                    state = State(self.currentState.row+self.dictDir[action][0],self.currentState.col+self.dictDir[action][1])
                    self.path.pop(0)
                    return action,state
            action = self.dfsPath[0]
            state = State(self.currentState.row+self.dictDir[action][0],self.currentState.col+self.dictDir[action][1])
            self.dfsPath.pop(0)
            return action,state
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

