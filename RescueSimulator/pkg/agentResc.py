import sys
import os

## Importa Classes necessarias para o funcionamento
from model import Model
from problem import Problem
from state import State
from localSearch import LocalSearch

class AgentResc:
    def __init__(self,model,configDict,prob,stateMesh):
        #guarda a instância de model para se movimentar (executeGo) e ler a posição atual.
        self.model = model

        ## Obtem o tempo que tem para executar
        self.tl = configDict["Ts"]
        print("Tempo disponivel: ", self.tl)
        
        ## Pega o tipo de mesh, que está no model (influência na movimentação)
        self.mesh = self.model.mesh
 
        ## Cria a instância do problema na mente do agente (sao suas crencas)
        self.prob = prob

        self.stateMesh = stateMesh
        # O agente le sua posica no ambiente por meio do sensor
        initial = self.positionSensor()
        self.prob.defGoalState(-1,-1)
        print("*** Estado inicial do agente: ", self.prob.initialState)
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        #print("*** Objetivo do agente: ", self.prob.goalState)
        
        ## Custo da solução
        self.costAll = 0
        
        self.plan = LocalSearch(model,initial,self.prob,self.stateMesh)

        ## inicializa acao do ciclo anterior com o estado esperado
        self.previousAction = "nop"    ## nenhuma (no operation)
        self.expectedState = self.currentState

        self.victims = []

    ## Metodo que define a deliberacao do agente 
    def deliberate(self):

        print("\n*** Inicio do ciclo raciocinio ***")
        print("Pos agente no amb.: ", self.positionSensor())

        ## Redefine o estado atual do agente de acordo com o resultado da execução da ação do ciclo anterior
        self.currentState = self.positionSensor()
        #self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano

        print("Ag cre que esta em: ", self.currentState)

        ## Funcionou ou nao, vou somar o custo da acao com o total 
        self.costAll += self.prob.getActionCost(self.previousAction)
        print ("Custo até o momento (com a ação escolhida):", self.costAll) 

        ## Verifica se tem vitima na posicao atual    
        victimId = self.victimPresenceSensor()

        if victimId > 0:
            print ("vitima encontrada em ", self.currentState, " id: ", victimId, " sinais vitais: ", self.victimVitalSignalsSensor(victimId))
            print ("vitima encontrada em ", self.currentState, " id: ", victimId, " dif de acesso: ", self.victimDiffOfAcessSensor(victimId))  
            

        ## consome o tempo gasto
        self.tl -= self.prob.getActionCost(self.previousAction)
        
        print("Tempo disponivel: ", self.tl)
        #self.plan.updateTimeLeft(self.tl)

        ## Verifica se atingiu o estado objetivo
        if self.prob.goalTest(self.currentState):
            print("!!! Objetivo atingido !!!")
            return 0
            
        ## Executa esse acao, atraves do metodo executeGo 
        #TODOO
        #self.executeGo(result[0])
        #self.previousAction = result[0]
        #self.expectedState = result[1]       
        return 1

    ## Metodo que executa as acoes
    def executeGo(self, action):
        """Atuador: solicita ao agente físico para executar a acao.
        @param direction: Direcao da acao do agente {"N", "S", ...}
        @return 1 caso movimentacao tenha sido executada corretamente """

        ## Passa a acao para o modelo
        result = self.model.go(action)
        
        ## Se o resultado for True, significa que a acao foi completada com sucesso, e ja pode ser removida do plano
        ## if (result[1]): ## atingiu objetivo ## TACLA 20220311
        ##    del self.plan[0]
        ##    self.actionDo((2,1), True)
            

    ## Metodo que pega a posicao real do agente no ambiente
    def positionSensor(self):
        """Simula um sensor que realiza a leitura do posição atual no ambiente.
        @return instancia da classe Estado que representa a posição atual do agente no labirinto."""
        pos = self.model.agentPos
        return State(pos[0],pos[1])

    def victimPresenceSensor(self):
        """Simula um sensor que realiza a deteccao de presenca de vitima na posicao onde o agente se encontra no ambiente
           @return retorna o id da vítima"""     
        return self.model.isThereVictim()

    def victimVitalSignalsSensor(self, victimId):
        """Simula um sensor que realiza a leitura dos sinais da vitima 
        @param o id da vítima
        @return a lista de sinais vitais (ou uma lista vazia se não tem vítima com o id)"""     
        return self.model.getVictimVitalSignals(victimId)

    def victimDiffOfAcessSensor(self, victimId):
        """Simula um sensor que realiza a leitura dos dados relativos à dificuldade de acesso a vítima
        @param o id da vítima
        @return a lista dos dados de dificuldade (ou uma lista vazia se não tem vítima com o id)"""     
        return self.model.getDifficultyOfAcess(victimId)
    
    ## Metodo que atualiza a biblioteca de planos, de acordo com o estado atual do agente
    def updateLibPlan(self):
        for i in self.libPlan:
            i.updateCurrentState(self.currentState)

    def actionDo(self, posAction, action = True):
        self.model.do(posAction, action)

    def setVictims(self,victims):
        self.plan.calcMinVictimsDist(victims)
        self.victims = victims