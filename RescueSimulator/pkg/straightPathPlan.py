from random import randint
from state import State

class StraightPathPlan:

    def __init__(self, initialState, name = "none", mesh = "square"):

        self.walls = []
        self.initialState = initialState
        self.currentState = initialState
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
        """
        if(self.isPossibleToMove(State(self.currentState.row,self.currentState.col+self.goingRight))):
            return col,State(self.currentState.row,self.currentState.col+self.goingRight)
        else:
            self.goingRight*=-1
            if(self.isPossibleToMove(State(self.currentState.row+self.goingDown,self.currentState.col))):
                return row,State(self.currentState.row+self.goingDown,self.currentState.col)
            else:
                self.goingDown *=-1 
        """
        return col,State(self.currentState.row,self.currentState.col+self.goingRight)
    
    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
