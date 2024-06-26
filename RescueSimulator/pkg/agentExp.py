import sys
import os

## Importa Classes necessarias para o funcionamento
from dfsPlan import DFSPlan
from state import State

## Classe que define o Agente
class AgentExplorer:
    def __init__(self, model, configDict,prob,stateMesh):
        #guarda a instância de model para se movimentar (executeGo) e ler a posição atual.
        self.model = model

        #Estado : procurando vítimas (searching) ou voltando (returning)
        self.state = "searching"

        ## Obtem o tempo que tem para executar
        self.tl = configDict["Tl"]
        self.t = self.tl
        print("Tempo disponivel: ", self.tl)
        
        ## Pega o tipo de mesh, que está no model (influência na movimentação)
        self.mesh = self.model.mesh
 
        ## Cria a instância do problema na mente do agente (sao suas crencas)
        self.prob = prob

        self.stateMesh  = stateMesh

        # O agente le sua posica no ambiente por meio do sensor
        initial = self.positionSensor()
        self.prob.defInitialState(initial.row, initial.col)
        self.prob.defGoalState(-1,-1)
        print("*** Estado inicial do agente: ", self.prob.initialState)
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Inicializa uma crença do labirinto que o agente possui. Isto é, ele sabe que o tamanho do mapa é no mínimo 
        # tão grande quanto a sua posição inicial.
        self.prob.createMaze(self.currentState.row+1,self.currentState.col+1)

        #print("*** Objetivo do agente: ", self.prob.goalState)
        print("*** Total de vitimas existentes no ambiente: ", self.model.getNumberOfVictims())

        """
        DEFINE OS PLANOS DE EXECUÇÃO DO AGENTE
        """
        
        ## Custo da solução
        self.costAll = 0
        
        self.plan = DFSPlan(initial,self.stateMesh, self.mesh,self.prob)
        
        ## Adiciona o(s) planos a biblioteca de planos do agente
        self.libPlan=[self.plan]

        ## inicializa acao do ciclo anterior com o estado esperado
        self.previousAction = "nop"    ## nenhuma (no operation)
        self.expectedState = self.currentState

        self.victims = []

        self.victimsID = []
    ## Metodo que define a deliberacao do agente 
    def deliberate(self):
        ## Verifica se há algum plano a ser executado
        if len(self.libPlan) == 0:
            return -1   ## fim da execucao do agente, acabaram os planos
        
        self.plan = self.libPlan[0]

        ## Redefine o estado atual do agente de acordo com o resultado da execução da ação do ciclo anterior
        self.currentState = self.positionSensor()
        self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano

        ## Verifica se a execução do acao do ciclo anterior funcionou ou nao
        if not (self.currentState == self.expectedState):
            print("---> erro na execucao da acao ", self.previousAction, ": esperava estar em ", self.expectedState, ", mas estou em ", self.currentState)
            self.prob.setWall(self.expectedState.row,self.expectedState.col)
        else:
            self.prob.setPath(self.currentState.row,self.currentState.col)

        ## Funcionou ou nao, vou somar o custo da acao com o total 
        self.costAll += self.prob.getActionCost(self.previousAction)

        ## Verifica se tem vitima na posicao atual    
        victimId = self.victimPresenceSensor()
        if victimId > 0:
            if victimId not in self.victimsID:
                print ("vitima encontrada em ", self.currentState, " id: ", victimId, " sinais vitais: ", self.victimVitalSignalsSensor(victimId))
                self.tl-=2
                self.victims.append({'id':victimId,'pos':self.currentState,'vit':self.victimVitalSignalsSensor(victimId)})
                self.victimsID.append(victimId)

        ## consome o tempo gasto
        self.tl -= self.prob.getActionCost(self.previousAction)
        
        print("Tempo disponivel: ", self.tl)
        state = self.plan.updateTimeLeft(self.tl)
        if (state == 1 and self.state == 'searching'):
            self.state = 'returning'
            self.prob.defGoalState(self.prob.initialState.row,self.prob.initialState.col) 

        ## Verifica se atingiu o estado objetivo
        if self.prob.goalTest(self.currentState):
            print("!!! Objetivo atingido !!!")
            del self.libPlan[0]  ## retira plano da biblioteca

            print('Porcentual de vítimas encontradas:'+ str(len(self.victims)/self.model.getNumberOfVictims()))
            print('tempo gasto pelo As por vítima salva: ' + str((self.t-self.tl)/len(self.victims)))
            print('Porcentual ponderado de vítimas encontradas por extrato de gravidade: ' + str(self.calcScore()))
            print('\n')
            return 0
            
        ## Define a proxima acao a ser executada
        ## currentAction eh uma tupla na forma: <direcao>, <state>
        result = self.plan.chooseAction()

        ## Executa esse acao, atraves do metodo executeGo 
        self.executeGo(result[0])
        self.previousAction = result[0]
        self.expectedState = result[1]       
        self.prob.updateMazeBelief(self.expectedState.row,self.expectedState.col)
        #self.prob.printMazeBelief()
        return 1
    def calcScore(self):
        victimsSignals = []
        for victim in self.victimsID:
            victimsSignals.append(self.victimVitalSignalsSensor(victim))
        victiomsConditions = [0 for i in range(4)]
        for victim in victimsSignals:
            if victim<=0.25:
                victiomsConditions[0] +=1
                continue
            elif victim<=0.50:
                victiomsConditions[1] +=1
                continue
            elif victim<=0.75:
                victiomsConditions[2] +=1
                continue
            else:
                victiomsConditions[3] +=1
                continue
        num = 4*victiomsConditions[0]+ 3*victiomsConditions[1] + 2*victiomsConditions[2] +victiomsConditions[3]
        den = 4*self.model.getVictimsCondition()[0]+ 3*self.model.getVictimsCondition()[1] + 2*self.model.getVictimsCondition()[2] +self.model.getVictimsCondition()[3]
        return float(num)/den
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
        return self.model.getVictimVitalSignals(victimId)[0][-1]
    
    ## Metodo que atualiza a biblioteca de planos, de acordo com o estado atual do agente
    def updateLibPlan(self):
        for i in self.libPlan:
            i.updateCurrentState(self.currentState)

    def actionDo(self, posAction, action = True):
        self.model.do(posAction, action)

    def getVictims(self):
        return self.victims