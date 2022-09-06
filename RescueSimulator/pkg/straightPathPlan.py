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
        def __init__(self):
            self.neighbors = {}
        def add_neighbor(self,node,dir):
            self.neighbors[dir] = node
            node.neighbors[self.revDir[dir]] = self

    dictDir = {
        'N':State(-1,0),
        'S':State(1,0),
        'L':State(0,1),
        'O':State(0,-1),
        'NO':State(-1,-1),
        'NL':State(-1,1),
        'SO':State(1,-1),
        'SL':State(1,1)
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
        self.dictDir = {}
        self.dictDir[(0,0)] = self.Node()

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
        #self.upShortestWayback()
        
    #Calcula o melhor caminho para voltar.
    def upGraph(self):
        posDir = self.posDirections(self.currentState)
        if (self.currentState.row,self.currentState.col) not in self.dictDir:
            self.dictDir[(self.currentState.row,self.currentState.col)] = self.Node()
        curNode = self.dictDir[(self.currentState.row,self.currentState.col)]
        for dir in posDir:
            curNode.add_neighbor(self.dictDir[dir[1]],dir[0])

    def upShortestWayback(self):
        pass
        #self.a_star_algorithm()
        
    def a_star_algorithm(self):
        #Direções possíveis a partir do estado atual do agente.
        posDir = self.posDirections(self.currentState)

        #inicia uma arvore de busca
        tree = self.Node(None,0,'',State(self.currentState.row,self.currentState.col))
        goal = State(self.initialState.row,self.initialState.col)

        #Estimativas de cada nó (dict[node] = estimativa)
        heurs = {}
        
        for dir in posDir:
            cost = dir[1]
            heur = self.calcHeuristic(dir[2][0],dir[2][1])
            node = self.Node(tree,cost,dir[0],State(dir[2][0],dir[2][1]))
            heurs[node] = cost+heur

        #Quando não há ações possíveis(quando o agente inicia no estudo alvo, por exemplo)
        if(len(heurs) == 0):
            return

        #nó atual (current)
        cur = min(heurs,key=heurs.get)
        del heurs[cur]

        #Se o caminho que ele manda ir é o caminho que já havia sido computado.
        #if len(self.wayBack)!=0 and cur.dir == self.wayBack[-1]:
        #    self.wayBack.append(cur.dir)
        #    return

        #Enquanto ele não acha o caminho de volta
        while(cur.state!=goal):
            posDir = self.posDirections(cur.state)
            for dir in posDir:
                cost = dir[1]+cur.cost
                heur = self.calcHeuristic(dir[2][0],dir[2][1])
                node = self.Node(cur,cost,dir[0],State(dir[2][0],dir[2][1]))
                heurs[node] = cost+heur
            cur = min(heurs,key=heurs.get)
            del heurs[cur]

        self.wayBack = []
    
        while cur.father!=None:
            self.wayBack.append(cur.dir)
            cur = cur.father

    def calcHeuristic(self,row,col):
        return math.sqrt(math.pow((row-self.initialState.row),2)+math.pow((col-self.initialState.col),2))

    #Direções que o agente pode ir de acordo com a sua crença do mapa. Retorna também o custo para ir em determinada direção
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
    
     


        
       
        
        
