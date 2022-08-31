from random import randint
from state import State

class StraightPathPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []

        self.goingRight = 1
        self.goingDown = 1

    
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
         self.currentState = state

    def isPossibleToMove(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """


        ## vai para fora do labirinto
        if (toState.col < 0 or toState.row < 0):
            return False

        if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
            return False
        
        if len(self.walls) == 0:
            return True
        
        ## vai para cima de uma parede
        if (toState.row, toState.col) in self.walls:
            return False

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = toState.row - self.currentState.row
        delta_col = toState.col - self.currentState.col

        ## o movimento eh na diagonal
        if (delta_row !=0 and delta_col != 0):
            if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
                return False
        
        return True

    def randomizeNextPosition(self):
         """ Sorteia uma direcao e calcula a posicao futura do agente 
         @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
         possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
         movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}

         rand = randint(0, 7)
         movDirection = possibilities[rand]
         state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])

         return movDirection, state

    def chooseAction(self):
        col = "L"  if self.goingRight == 1 else "O"
        row = "S"  if self.goingDown == 1 else "N"
        
        if(self.isPossibleToMove(State(self.currentState.row,self.currentState.col+self.goingRight))):
            return col,State(self.currentState.row,self.currentState.col+self.goingRight)
        else:
            self.goingRight*=-1
            if(self.isPossibleToMove(State(self.currentState.row+self.goingDown,self.currentState.col))):
                return row,State(self.currentState.row+self.goingDown,self.currentState.col)
            else:
                self.goingDown *=-1


    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
