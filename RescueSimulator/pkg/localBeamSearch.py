from copy import deepcopy
from aStar import AStar
import random

class LocalBeamSearch():

    def __init__(self,model,initialState,prob,stateMesh):
        self.initialState = initialState
        self.currentState = initialState

        self.prob = prob
        
        self.victDist = {}
        self.distVictGoal = {}
        self.aStar = AStar()
        self.stateMesh = stateMesh
        self.victims = []
        self.model = model

    def calcMinVictimsDist(self,victims:list):
        if(len(victims) == 0):
            return -1
        self.victims = victims
        print('Calculando Distância entre as Vítimas...')
        for v1 in range(len(victims)-1):
            self.victDist[(v1,-1)] = self.aStar.a_star_algorithm(
                    (victims[v1]['pos'].row,victims[v1]['pos'].col),
                    (self.initialState.row,self.initialState.col),
                    self.stateMesh
                ) 
            self.victDist[(-1,v1)] = self.aStar.a_star_algorithm(
                    (self.initialState.row,self.initialState.col),
                    (victims[v1]['pos'].row,victims[v1]['pos'].col),
                    self.stateMesh
                ) 
            for v2 in range(v1+1,len(victims)):
                self.victDist[(v1,v2)] = self.aStar.a_star_algorithm(
                    (victims[v1]['pos'].row,victims[v1]['pos'].col),
                    (victims[v2]['pos'].row,victims[v2]['pos'].col),
                    self.stateMesh
                )  
                self.victDist[(v2,v1)] = self.reversePath(self.victDist[(v1,v2)][0]),self.victDist[(v1,v2)][1]
            print(f'{v1/len(victims)*100:.2f}%',end="\r")
        self.victDist[(len(victims)-1,-1)] = self.aStar.a_star_algorithm(
                    (victims[len(victims)-1]['pos'].row,victims[len(victims)-1]['pos'].col),
                    (self.initialState.row,self.initialState.col),
                    self.stateMesh
                )
        self.victDist[(-1,len(victims)-1)] = self.aStar.a_star_algorithm(
                    (self.initialState.row,self.initialState.col),
                    (victims[len(victims)-1]['pos'].row,victims[len(victims)-1]['pos'].col),
                    self.stateMesh)
              
        return 1

    def reversePath(self,path):
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
        revP = []
        for p in path:
            revP.append(revDir[p])
        return list(reversed(revP))
        
    def createSolution(self,ts:list=None):
        v = list(range(len(self.victims)))
        solution = []

        while self.calcCostSolution(solution)<=ts and len(v)>0:
            randVic = random.choice(v)
            v.remove(randVic)
            solution.append(randVic)       
        solCost = self.calcCostSolution(solution)
        if(solCost>ts):
            solution.pop()
            solCost = self.calcCostSolution(solution)
        return solution

    def calcCostSolution(self,solution):
        cost = 0
        if len(solution) == 0:
            return 0

        for i in range(len(solution)-1):
            cost+=self.victDist[(solution[i],solution[i+1])][1]
        cost+=self.victDist[(solution[-1],-1)][1]
        cost+=self.victDist[(-1,solution[0])][1]
        return cost

    def evaluateSolution(self,solution:list):
        victiomsConditions = [0 for i in range(4)]
        for victim in solution:
            if self.victims[victim]['vit']<=0.25:
                victiomsConditions[0] +=1
                continue
            elif self.victims[victim]['vit']<=0.50:
                victiomsConditions[1] +=1
                continue
            elif self.victims[victim]['vit']<=0.75:
                victiomsConditions[2] +=1
                continue
            else:
                victiomsConditions[3] +=1
                continue
        num = 4*victiomsConditions[0]+ 3*victiomsConditions[1] + 2*victiomsConditions[2] +victiomsConditions[3]
        den = 4*self.model.getVictimsCondition()[0]+ 3*self.model.getVictimsCondition()[1] + 2*self.model.getVictimsCondition()[2] +self.model.getVictimsCondition()[3]
        return float(num)/den
    
    def createNeighbours(self,solution:list,num,ts):
        neighbours = []
        
        if(len(solution) == len(self.victims)):
            return []

        for i in range(num):
            vAux = list(range(len(self.victims)))
            vicNeighbours = [v for v in vAux if v not in solution]

            if(len(solution)==0):
                new = random.choice(vicNeighbours)
                newNeighbour = []
                newNeighbour.append(new)
            else:
                rem = random.choice(solution)
                new = random.choice(vicNeighbours)
        
                newNeighbour = deepcopy(solution)
                newNeighbour[newNeighbour.index(rem)] = new

            cost = self.calcCostSolution(newNeighbour) 

            if cost<=ts:
                neighbours.append(newNeighbour)
        return neighbours
        
    def swapNeighbours(self,neighbours,ts,numSwap):
        newNeighbours = []
        
        for neighbour in neighbours:
            for i in range(numSwap):
                if(len(neighbour)<=1):
                    continue
                newNeighbour = deepcopy(neighbour)
                randVict = random.sample(list(range(len(newNeighbour))),2)
                newNeighbour[randVict[0]],newNeighbour[randVict[1]] = newNeighbour[randVict[1]],newNeighbour[randVict[0]]
                if self.calcCostSolution(newNeighbour)<=ts:
                    newNeighbours.append(newNeighbour)  
        return newNeighbours

    def addVictim(self,neighbours,ts):
        for n in range(len(neighbours)):
            vAux = list(range(len(self.victims)))
            vicNeighbours = [v for v in vAux if v not in neighbours[n]]
            while len(vicNeighbours)>0:
                newNeighbour = deepcopy(neighbours[n])
                
                new = random.choice(vicNeighbours)
                newNeighbour.append(new)
                vicNeighbours.remove(new)

                if self.calcCostSolution(newNeighbour)<=ts:
                    neighbours[n] = newNeighbour
                    break

    def chooseBestNeighbours(self,solution:list,num,ts,numSwap = 1):

        #Tira num da solução, e escolhe num novos vizinhos.
        neighbours = self.createNeighbours(solution,num,ts)
        neighbours.append(solution)
        
        #Troca duas vítimas de posição
        neighbours += self.swapNeighbours(neighbours,ts,numSwap)
        self.addVictim(neighbours,ts)

        eval = [self.evaluateSolution(solution) for solution in neighbours]

        maxEval = max(eval)
        indexBest = eval.index(maxEval)
        return neighbours[indexBest],maxEval

    def localSearch(self,ts,nSolutions:int=20,nNei=5,numIt=100,numSwaps = 1):
        solutions = []
        eval = []

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

        for i in range(nSolutions):
            sol = self.createSolution(ts)
            solutions.append(sol)
            eval.append(self.evaluateSolution(sol))

        print('Calculando Trajetória...')
        for i in range(numIt):
            for sol in range(len(solutions)):
                bestNeighbour = self.chooseBestNeighbours(solutions[sol],nNei,ts,numSwaps)
                solutions[sol] = bestNeighbour[0]
                eval[sol] = bestNeighbour[1]
            maxEval = max(eval)
            print(f'{i/numIt*100:.2f}%',end="\r")

        maxEval = max(eval)
        print('Score:' + str(maxEval))
        indexBest = eval.index(maxEval)
        path = self.createPath(solutions[indexBest])

        return path

    def createPath(self,solution):
        if(len(solution)==0):
            return ''

        path = []
        path += self.victDist[(-1,solution[0])][0]
        for i in range(len(solution)-1):
            path+=self.victDist[(solution[i],solution[i+1])][0]
        path += self.victDist[(solution[-1],-1)][0]
        return path