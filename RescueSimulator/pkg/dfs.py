from typing import Tuple
from stateMesh import StateMesh
from state import State
from aStar import AStar

class DFS:
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
	class Node:
		def __init__(self,state,parent = None):
			self.parent = None
			self.state = state
			
	def __init__(self,initialState:Tuple,prob,stateMesh:StateMesh = None):
		self.prob = prob
		self.stack = []
		self.nodeDict = {}
		self.visitedNodes = []
		self.curNode = self.Node(initialState)	
		self.prevNode = self.Node(initialState)	
		self.nodeDict[(initialState[0],initialState[1])] = self.curNode
		self.firstStep = True
		self.aStar = AStar()
		self.stateMesh = stateMesh

		self.createNodeFunctions = {}
		self.stackOrderCardinal = ['L','N','O','S']
		self.stackOrderOrdinal = ['SE','NO','NE','SO']

		self.lastMovement = ''
		self.initNodeCreationFunctions()

	def dfs(self,state:Tuple):
		#Se ele bateu em uma parede.
		if (state == self.prevNode.state and not self.firstStep):

			#Pega o próximo nó a ser expandido
			nextNode = self.stack[-1]
			self.stack.pop()

			#Enquanto não acha um nó ainda não visitado.
			while(nextNode[1] in self.visitedNodes):
				nextNode = self.stack[-1]
				self.stack.pop()

			#Define o pai do nó a ser expandido como destino.
			goalState = nextNode[2].state
			initialState = state
			path = []
			#Se o estado atual é diferente do pai do nó a ser expandido
			if(goalState != initialState):
				path = self.aStar.a_star_algorithm(initialState,goalState,self.stateMesh)[0]
			else:
				pass
			self.prevNode =  nextNode[2]
			#Adiciona o caminho para se atingir o nó destino a partir do nó pai.
			path.append(nextNode[0])
			self.curNode = nextNode[1]
			self.updateStackOrder(hitWall=True,nextAction = nextNode[0])
			self.lastMovement = nextNode[0]
			return path

		
		if self.firstStep:
			self.firstStep = False
		else:
			self.updateStackOrder(hitWall=False)
		
		nodes = self.createPosNodes(self.curNode)

		#Se é um nó folha.
		if(len(nodes)==0):
			
			nextNode = self.stack[-1]
			self.stack.pop()

			while(nextNode[1] in self.visitedNodes):
				nextNode = self.stack[-1]
				self.stack.pop()

			goalState = nextNode[2].state
			initialState = self.curNode.state
			path = []
			if(goalState != initialState):
				path = self.aStar.a_star_algorithm(initialState,goalState,self.stateMesh)[0]
			self.prevNode =  nextNode[2]
			path.append(nextNode[0])
			self.curNode = nextNode[1]
			self.visitedNodes.append(nextNode[1])
			self.lastMovement = nextNode[0]
			return path

		self.stack += nodes
		nextNode = self.stack[-1]
		self.stack.pop()

		while(nextNode[1] in self.visitedNodes):
				nextNode = self.stack[-1]
				self.stack.pop()

		self.prevNode = self.curNode
		self.curNode = nextNode[1]
		self.visitedNodes.append(nextNode[1])
		self.lastMovement = nextNode[0]
		return [nextNode[0]]

	def updateStackOrder(self,hitWall,nextAction = None):
		if(hitWall):
			index = self.stackOrderCardinal.index(self.lastMovement)
			self.stackOrderCardinal[0],self.stackOrderCardinal[index] = self.stackOrderCardinal[index],self.stackOrderCardinal[0] 
		else:
			index = self.stackOrderCardinal.index(self.lastMovement)
			self.stackOrderCardinal[3],self.stackOrderCardinal[index] = self.stackOrderCardinal[index],self.stackOrderCardinal[3] 

	def createPosNodes(self,curNode):
		nodes = []
		for dir in self.stackOrderCardinal:
			self.createNodeFunctions[dir](self,curNode,nodes)
		for dir in self.stackOrderOrdinal:
			self.createNodeFunctions[dir](self,curNode,nodes)	
		return nodes

	def initNodeCreationFunctions(self):
		def createNodeNE(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]][curNode.state[1]+2] == 0 and self.prob.mazeBelief[curNode.state[0]][curNode.state[1]+1]==1 and self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]+2]==1:
				if (curNode.state[0]-1,curNode.state[1]+1) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0]-1,curNode.state[1]+1)] = self.Node((curNode.state[0]-1,curNode.state[1]+1),curNode)
				nodes.append(('NE',self.nodeDict[(curNode.state[0]-1,curNode.state[1]+1)],curNode))
		self.createNodeFunctions['NE'] = createNodeNE
		def createNodeNO(self,curNode,nodes):		
			if self.prob.mazeBelief[curNode.state[0]][curNode.state[1]] == 0 and self.prob.mazeBelief[curNode.state[0]][curNode.state[1]+1]==1 and self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]]==1 :
				if (curNode.state[0]-1,curNode.state[1]-1) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0]-1,curNode.state[1]-1)] = self.Node((curNode.state[0]-1,curNode.state[1]-1),curNode)
				nodes.append(('NO',self.nodeDict[(curNode.state[0]-1,curNode.state[1]-1)],curNode))
		self.createNodeFunctions['NO'] = createNodeNO
		def createNodeSO(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]] == 0 and self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]]==1 and self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]+1]==1 :
				if (curNode.state[0]+1,curNode.state[1]-1) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0]+1,curNode.state[1]-1)] = self.Node((curNode.state[0]+1,curNode.state[1]-1),curNode)
				nodes.append(('SO',self.nodeDict[(curNode.state[0]+1,curNode.state[1]-1)],curNode))
		self.createNodeFunctions['SO'] = createNodeSO
		def createNodeSE(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]+2] == 0 and self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]+2]==1 and self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]+1]==1:
				if (curNode.state[0]+1,curNode.state[1]+1) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0]+1,curNode.state[1]+1)] = self.Node((curNode.state[0]+1,curNode.state[1]+1),curNode)
				nodes.append(('SE',self.nodeDict[(curNode.state[0]+1,curNode.state[1]+1)],curNode))	
		self.createNodeFunctions['SE'] = createNodeSE
		def createNodeN(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]][curNode.state[1]+1] == 0:
				if (curNode.state[0]-1,curNode.state[1]) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0]-1,curNode.state[1])] = self.Node((curNode.state[0]-1,curNode.state[1]),curNode)
				nodes.append(('N',self.nodeDict[(curNode.state[0]-1,curNode.state[1])],curNode))
		self.createNodeFunctions['N'] = createNodeN
		def createNodeL(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]+2] == 0:
				if (curNode.state[0],curNode.state[1]+1) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0],curNode.state[1]+1)] = self.Node((curNode.state[0],curNode.state[1]+1),curNode)
				nodes.append(('L',self.nodeDict[(curNode.state[0],curNode.state[1]+1)],curNode))
		self.createNodeFunctions['L'] = createNodeL
		def createNodeS(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]+1] == 0:
				if (curNode.state[0]+1,curNode.state[1]) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0]+1,curNode.state[1])] = self.Node((curNode.state[0]+1,curNode.state[1]),curNode)
				nodes.append(('S',self.nodeDict[(curNode.state[0]+1,curNode.state[1])],curNode))
		self.createNodeFunctions['S'] = createNodeS
		def createNodeO(self,curNode,nodes):
			if self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]] == 0:
				if (curNode.state[0],curNode.state[1]-1) not in self.nodeDict.keys():
					self.nodeDict[(curNode.state[0],curNode.state[1]-1)] = self.Node((curNode.state[0],curNode.state[1]-1),curNode)
				nodes.append(('O',self.nodeDict[(curNode.state[0],curNode.state[1]-1)],curNode))
		self.createNodeFunctions['O'] = createNodeO

