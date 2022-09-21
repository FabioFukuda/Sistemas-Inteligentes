from copy import deepcopy
from agentExp import AgentExplorer
from agentResc import AgentResc
from maze import Maze
from localSearch import LocalSearch
from problem import Problem
from stateMesh import StateMesh
from state import State
import random

import pandas as pd
import matplotlib.pyplot as plt
import time
import os

class TesteBuscaLocal():
    def __init__(self,model,configDict):
        #Lista de agentes
        self.prob = Problem()
        self.stateMesh = StateMesh()

        self.maxR =  model.maze.maxRows
        self.maxC = model.maze.maxColumns
        self.maze = deepcopy(model.maze.walls)
        self.mazeBelief = [[0 for j in range(self.maxC)] for i in range(self.maxR)]  
        self.model = model
        self.victims = []
        self.victimsID = []
        self.createFullMesh()

        self.model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
        self.initialState = State(model.maze.board.posAgent[0],model.maze.board.posAgent[1])

    def execute(self):
        numVitimas = 15
        numMinIt = 0
        numMaxIt = 100
        numVizinhos = 20
        ts = 100

        plt.ioff()
        dados = {'numIt':[],'score':[],'tempo':[]}
        
        chosenV,chosenVId = self.randomVictims(numVitimas)
        buscaAux = LocalSearch(self.model,self.initialState,self.prob,self.stateMesh)
        buscaAux.calcMinVictimsDist(chosenV)
        victDist = buscaAux.victDist

        for i in range(numMinIt,numMaxIt):
            print(f'Iterção Número:{i}')
            local = LocalSearch(self.model,self.initialState,self.prob,self.stateMesh)
            local.victDist = victDist
            local.victims = chosenV

            start_time = time.time()
            eval = local.localSearch(ts,numVizinhos,i,True)
            timeDif = time.time() - start_time

            dados['numIt'].append(i)
            dados['score'].append(eval)
            dados['tempo'].append(timeDif)

        dataFrame = pd.DataFrame(dados)
        path = os.path.join("resultados",str(numVitimas)+'Vitimas_' + str(numMinIt)+'-'+str(numMaxIt)+'_Iteracoes')
        
        plt.scatter(x=dataFrame['numIt'],y=dataFrame['score'])
        plt.savefig(path)
        
        return -1

    def randomVictims(self,numVict):
        vic = random.sample(list(range(len(self.victims))),numVict)

        chosenV = [vict for i,vict in enumerate(self.victims) if i in vic]
        chosenVId = [vict for i,vict in enumerate(self.victimsID) if i in vic]
        return chosenV,chosenVId
        
    def createFullMesh(self): 
        for r in range(self.maxR):
            for c in range(self.maxC):
                if self.maze[r][c] == 0:
                    self.mazeBelief[r][c] = 1
                    cur = State(r,c)    
                    posDir = self.posDirections(cur)
                    self.stateMesh.addNode(cur)
                    #Adiciona os vizinhos no nó
                    self.stateMesh.addNodeNeighbours(self.stateMesh.getNode((cur.row,cur.col)),posDir)
                    self.model.setAgentPos(r,c)
                    victimId = self.model.isThereVictim()
                    if victimId > 0:
                        if victimId not in self.victimsID:
                            self.victims.append({'id':victimId,'pos':cur,'vit': self.model.getVictimVitalSignals(victimId)[0][-1],'acc':self.model.getDifficultyOfAcess(victimId)[0][-1]})
                            self.victimsID.append(victimId)

    def posDirections(self,state):
        posDir = []
        if state.row-1>=0 and state.col-1>=0 and self.mazeBelief[state.row-1][state.col-1] == 1:
            posDir.append(('NO',(state.row-1,state.col-1)))
        if state.row-1>=0 and state.col>=0 and self.mazeBelief[state.row-1][state.col] == 1:
            posDir.append(('N',(state.row-1,state.col)))
        if state.row-1>=0 and state.col+1<self.maxC and self.mazeBelief[state.row-1][state.col+1] == 1:
            posDir.append(('NE',(state.row-1,state.col+1)))
        if state.row>=0 and state.col+1<self.maxC and self.mazeBelief[state.row][state.col+1] == 1:
            posDir.append(('L',(state.row,state.col+1)))
        if state.row+1<self.maxR and state.col+1<self.maxC and self.mazeBelief[state.row+1][state.col+1] == 1:
            posDir.append(('SE',(state.row+1,state.col+1)))
        if state.row+1<self.maxR and state.col>=0 and self.mazeBelief[state.row+1][state.col] == 1:
            posDir.append(('S',(state.row+1,state.col)))
        if state.row+1<self.maxR and state.col-1>=0 and self.mazeBelief[state.row+1][state.col-1] == 1:
            posDir.append(('SO',(state.row+1,state.col-1)))
        if state.row>=0 and state.col-1>=0 and self.mazeBelief[state.row][state.col-1] == 1:
            posDir.append(('O',(state.row,state.col-1)))
        return posDir