from copy import deepcopy
from stateMesh import StateMesh
from state import State

class AStar():
    
    #Classe auxiliar para manter os estados explorados no algoritmo A*.
    class AStarState:
        def __init__(self,state):
            #Encadeia os estados para a construção da solução.
            self.parent = None
            #Nó que o estado representa.
            self.state = state
            #Atributo auxiliar que mantém o custo até este nó durante a execução do A*.
            self.cost = 0.0
            #Direção do nó pai para este nó.
            self.dir = ''
            #States até este nó. Serve para evitar com que nó já visitados sejam incluidos novamente.
            self.path = []
        
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

    #Calcula o melhor caminho para voltar. Retorna uma lista com as direções da volta, e o tempo estimado.   
    def a_star_algorithm(self,goal:tuple,start:tuple,stateMesh:StateMesh):

        #Estimativas de cada estado que estão na borda (State:estimativa)
        est = {}
        #curNode = dictNode[()]

        #Cria um estado inicial para o algoritmo A*.
        curPos = start
        curAStarState = self.AStarState(curPos)
        
        minPathNode = {}
        borderNodes = {}

        minPathNode[curPos] = 0

        for dir,state in stateMesh.getNodeNeighborsTuple(curPos).items():
            heur = self.calcHeuristic(state,goal)
            cost = self.dictCost[dir]

            newAStarState = self.AStarState(state)
            newAStarState.parent = curAStarState
            newAStarState.cost = cost
            newAStarState.dir = self.revDir[dir]
            newAStarState.path.append(curPos)
            est[newAStarState] = heur+cost

            minPathNode[state] = cost
            borderNodes[newAStarState] = state
        if len(est) == 0:
            return [],0

        #Pega o estado com a menor estimativa na borda.
        curAStarState =  min(est, key=est.get)
        curPos = curAStarState.state
        
        del est[curAStarState]

        while(curPos!=goal):
            for dir,state in stateMesh.getNodeNeighborsTuple(curPos).items():
                #Se o estado já foi descoberto nesse ramo (evita loops).
                if state not in curAStarState.path:
                    heur = self.calcHeuristic(state,goal)

                    newAStarState = self.AStarState(state)
                    newAStarState.parent = curAStarState
                    newAStarState.cost = self.dictCost[dir]+curAStarState.cost
                    newAStarState.heur=heur
                    newAStarState.dir = self.revDir[dir]
                    #Cada estado mantém o caminho até ele
                    newAStarState.path = deepcopy(curAStarState.path)
                    newAStarState.path.append(state)
                 
                    if state in minPathNode.keys():
                        if newAStarState.cost>minPathNode[state]:
                            continue
                        else:
                            if state in borderNodes.values():
                                state = list(borderNodes.keys())[list(borderNodes.values()).index(state)]
                                del borderNodes[state]
                                del est[state]
                                 
                    est[newAStarState] = heur+newAStarState.cost
                    borderNodes[newAStarState] = state
                    minPathNode[state] = newAStarState.cost

            curAStarState =  min(est, key=est.get)
            curPos = curAStarState.state

            del est[curAStarState]
            del borderNodes[curAStarState]

        estTime = curAStarState.cost
        path = []
        while curAStarState.parent!=None:
            path.append(curAStarState.dir)
            curAStarState = curAStarState.parent
        return path, estTime

    def calcHeuristic(self,state1,state2):
        difR = abs(state1[0]-state2[0])
        difC = abs(state1[1]-state2[1])
        if(difR>difC):
            return 1.5*(difC) + (difR-difC) 
        else:
            return 1.5*(difR) + (difC-difR) 