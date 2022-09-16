from state import State

'''
Classe criada para  representar uma malha de estados, onde cada nó representa um estado (State). Assim, um nó se conecta ao outro
se ambos já foram visitados pelo agente.

A classe serve para verificar as ações possíveis em um determinado estado.'
'''

class StateMesh():
    def __init__(self):
        #Dict para acessar os nós (chave -> posição no mapa)
        self.dictNode = {}

    def addNode(self,state):
        self.dictNode[(state.row,state.col)] = Node(state)
    def getNode(self,pos):
        return self.dictNode[pos]
    def addNodeNeighbours(self,node,neighbours):
        for n in neighbours:
            node.add_neighbor(self.dictNode[n[1]],n[0])
    def getNodeNeighborsTuple(self,pos):
        return self.dictNode[pos].getNeighborsTuple()

    def __contains__(self, key):
        return key in self.dictNode

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
    
    def getNeighborsTuple(self):
        return {dir:(neighbors.state.row,neighbors.state.col) for dir,neighbors in self.neighbors.items()}
        