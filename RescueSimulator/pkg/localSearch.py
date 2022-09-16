from aStar import AStar
import random

class LocalSearch():
    def __init__(self,model,initialState,prob,stateMesh):
        self.initialState = initialState
        self.currentState = initialState

        self.prob = prob
        
        self.victDist = {}
        self.aStar = AStar()
        self.stateMesh = stateMesh
        self.victims = []
        self.model = model
    def calcMinVictimsDist(self,victims:list):
        self.victims = victims
        for v1 in range(len(victims)-1):
            for v2 in range(v1+1,len(victims)):
                self.victDist[(v1,v2)] = self.aStar.a_star_algorithm(
                    (victims[v1]['pos'].row,victims[v1]['pos'].col),
                    (victims[v2]['pos'].row,victims[v2]['pos'].col),
                    self.stateMesh
                )  
                self.victDist[(v2,v1)] = self.reversePath(self.victDist[(v1,v2)][0]),self.victDist[(v1,v2)][1]
        self.localSearch(150,20)
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
        return revP.reverse()
        
    def createSolution(self,ts):
        v = list(range(len(self.victims)))
        solution = []
        totCost = 0
        prevVic = 0

        randVic = random.choice(v)
        solution.append(randVic)
        v.remove(randVic)
        prevVic = randVic

        while totCost<=ts and len(v)>0:
            randVic = random.choice(v)
            cost = self.victDist[(prevVic,randVic)][1]
            if totCost+cost<ts:
                totCost+=cost
                solution.append(randVic)
                v.remove(randVic)
                prevVic = randVic
            else:
                return solution

        return solution

    def evaluateSolution(self,solution):
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
    def localSearch(self,ts,k:int):
        solutions = []
        eval = []
        for i in range(k):
            sol = self.createSolution(ts)
            solutions.append(sol)
            eval.append(self.evaluateSolution(sol))
        pass