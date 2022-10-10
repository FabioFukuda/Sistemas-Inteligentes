import sys
import os

## Importa Classes necessarias para o funcionamento
from model import Model
from problem import Problem
from state import State
from rescuePlan import RescuePlan

class AgentResc:
    def __init__(self,model,configDict,prob,stateMesh):
        #guarda a instância de model para se movimentar (executeGo) e ler a posição atual.
        self.model = model

        ## Obtem o tempo que tem para executar
        self.ts = configDict["Ts"]
        self.t = self.ts
        print("Tempo disponivel: ", self.ts)
        
        ## Pega o tipo de mesh, que está no model (influência na movimentação)
        self.mesh = self.model.mesh
 
        ## Cria a instância do problema na mente do agente (sao suas crencas)
        self.prob = prob

        self.stateMesh = stateMesh
        # O agente le sua posica no ambiente por meio do sensor
        initial = self.positionSensor()
        self.prob.defInitialState(initial.row, initial.col)
        print("*** Estado inicial do agente: ", self.prob.initialState)
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        #print("*** Objetivo do agente: ", self.prob.goalState)
        
        ## Custo da solução
        self.costAll = 0
        
        self.plan = RescuePlan(model,initial,self.stateMesh,self.prob)

        ## inicializa acao do ciclo anterior com o estado esperado
        self.previousAction = "nop"    ## nenhuma (no operation)
        self.expectedState = self.currentState

        self.victims = []
        self.rescVict = []
        
    def elaboratePlan(self):
        return self.plan.calcPath(self.ts,self.victims)

    ## Metodo que define a deliberacao do agente 
    def deliberate(self):

        #print("\n*** Inicio do ciclo raciocinio ***")
        #print("Pos agente no amb.: ", self.positionSensor())

        ## Redefine o estado atual do agente de acordo com o resultado da execução da ação do ciclo anterior
        self.currentState = self.positionSensor()
        #self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano

        #print("Ag cre que esta em: ", self.currentState)

        ## Funcionou ou nao, vou somar o custo da acao com o total 
        self.costAll += self.prob.getActionCost(self.previousAction)
        #print ("Custo até o momento (com a ação escolhida):", self.costAll) 

        ## Verifica se tem vitima na posicao atual    
        victimId = self.victimPresenceSensor()

        if victimId > 0 and victimId not in self.rescVict:
            print ("vitima encontrada em ", self.currentState, " id: ", victimId, " sinais vitais: ", self.victimVitalSignalsSensor(victimId)) 
            self.rescVict.append(victimId)
            
        ## consome o tempo gasto
        self.ts -= self.prob.getActionCost(self.previousAction)
        
        print("Tempo disponivel: ", self.ts)
        #self.plan.updateTimeLeft(self.tl)
        
        result = self.plan.chooseAction()
        #print("Ag deliberou pela acao: ", result[0], " o estado resultado esperado é: ", result[1])
        
        if(result[0]=='nop'):
            print("!!! Fim do plano !!!")
            print('Porcentual de vítimas encontradas:'+ str(len(self.rescVict)/self.model.getNumberOfVictims()))
            print(f'Score:{self.calcScore()}')
            print('tempo gasto pelo As por vítima salva:' + str((self.t-self.ts)/len(self.rescVict)))
        

            return -1
        
        self.executeGo(result[0])
        self.previousAction = result[0]
        self.expectedState = result[1]       
        return 1
    def calcScore(self):
        victimsSignals = []
        for victim in self.rescVict:
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
        self.victims = victims