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
        numMinVitimas = 5
        numMaxVitimas = 9

        numIt = 200

        numVizinhos = 20
        nSolutions = 20
        numSwaps = 50
        ts = 100
    
        for vizinho in range(numVizinhos):
            for swap in range(numSwaps):
                for j in range(numMinVitimas,numMaxVitimas):
                    chosenV,chosenVId = self.randomVictims(j)
                    buscaAux = LocalSearch(self.model,self.initialState,self.prob,self.stateMesh)
                    buscaAux.calcMinVictimsDist(chosenV)
                    victDist = buscaAux.victDist

                    local = LocalSearch(self.model,self.initialState,self.prob,self.stateMesh)
                    local.victDist = victDist
                    local.victims = chosenV

                    start_time = time.time()
                    eval = local.localSearch(ts,20,vizinho,numIt,swap,test=True)
                    timeDif = time.time() - start_time

                    newRowEval = pd.DataFrame(index=[],columns=['eval'])
                    newRowEval.loc[0,'eval'] = eval
                    newRow = pd.DataFrame.from_dict({'num_vitimas':[j],'num_vizinhos':[vizinho],'num_trocas':[swap],'tempo':[timeDif]})
                    newRow = pd.concat([newRow,newRowEval],axis=1)

                    resultados = pd.read_csv('analise.csv',sep=';')
                    resultados = pd.concat([resultados,newRow],axis=0)
                    resultados.to_csv('analise.csv',sep=';',index = False)


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