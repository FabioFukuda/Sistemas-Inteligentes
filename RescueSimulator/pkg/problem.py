from maze import Maze
from state import State
from cardinal import *


class Problem:
    """Representação de um problema a ser resolvido por um algoritmo de busca clássica.
    A formulação do problema - instância desta classe - reside na 'mente' do agente."""

    def __init__(self):
        self.initialState = State(0,0)
        self.goalState = State(0,0)

    def createMaze(self, maxRows, maxColumns):
        """Este método instancia um labirinto - representa o que o agente crê ser o labirinto.
        As paredes devem ser colocadas fora desta classe porque este.
        @param maxRows: máximo de linhas do labirinto.
        @param maxColumns: máximo de colunas do labirinto."""
        self.mazeBelief = [[0 for i in range(maxColumns)] for j in range(maxRows)]
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.cost = [[0.0 for j in range(maxRows*maxColumns)]for i in range(8)]

    def updateMazeBelief(self,row,col):
        if row+1 > self.maxRows:
            self.mazeBelief[row-1].append([0 for i in range(self.maxColumns)])
            self.maxRows = row+1
        if col+1 > self.maxColumns:
            for i in range(self.maxRows):
                self.mazeBelief[i].append(0)
            self.maxColumns = col+1

    def setWall(self,row,col):
        self.mazeBelief[row][col] = -1

    def defInitialState(self, row, col):
        """Define o estado inicial.
        @param row: linha do estado inicial.
        @param col: coluna do estado inicial."""
        self.initialState.row = row
        self.initialState.col = col

    def defGoalState(self, row, col):
        """Define o estado objetivo.
        @param row: linha do estado objetivo.
        @param col: coluna do estado objetivo."""
        self.goalState.row = row
        self.goalState.col = col

    def getActionCost(self, action):
        """Retorna o custo da ação.
        @param action:
        @return custo da ação"""
        if (action=="nop"):
            return 0

        if (action == "N" or action == "L" or action == "O" or action == "S"):   
            return 1.0
        
        return 1.5

    def goalTest(self, currentState):
        """Testa se alcançou o estado objetivo.
        @param currentState: estado atual.
        @return True se o estado atual for igual ao estado objetivo."""
        if currentState == self.goalState:
            return True
        else:
            return False

    def printMazeBelief(self):

        print('Mapa estimado pelo agente:')
        for i in range(self.maxRows):
            col = ""
            for j in range(self.maxColumns):
                col += f'{self.mazeBelief[i][j]} '
            print(col)
                
