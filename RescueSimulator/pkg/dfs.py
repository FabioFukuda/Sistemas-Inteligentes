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

	def dfs(self,state:Tuple):
		if self.prevNode.state==(23,23):
			pass
		if (state == self.prevNode.state and not self.firstStep):
			nextNode = self.stack[-1]
			self.stack.pop()

			while(nextNode[1] in self.visitedNodes):
				nextNode = self.stack[-1]
				self.stack.pop()

			goalState = nextNode[2].state
			initialState = state
			path = []
			if(goalState != initialState):
				path = self.aStar.a_star_algorithm(initialState,goalState,self.stateMesh)[0]
			self.prevNode =  nextNode[2]
			path.append(nextNode[0])
			self.curNode = nextNode[1]
			
			return path

		if self.firstStep:
			self.firstStep = False

		nodes = self.createPosNodes(self.curNode)

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


		return [nextNode[0]]
		
	def createPosNodes(self,curNode):
		nodes = []	
		if self.prob.mazeBelief[curNode.state[0]][curNode.state[1]] == 0:
			if (curNode.state[0]-1,curNode.state[1]-1) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0]-1,curNode.state[1]-1)] = self.Node((curNode.state[0]-1,curNode.state[1]-1),curNode)
			nodes.append(('NO',self.nodeDict[(curNode.state[0]-1,curNode.state[1]-1)],curNode))
		if self.prob.mazeBelief[curNode.state[0]][curNode.state[1]+1] == 0:
			if (curNode.state[0]-1,curNode.state[1]) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0]-1,curNode.state[1])] = self.Node((curNode.state[0]-1,curNode.state[1]),curNode)
			nodes.append(('N',self.nodeDict[(curNode.state[0]-1,curNode.state[1])],curNode))
		if self.prob.mazeBelief[curNode.state[0]][curNode.state[1]+2] == 0:
			if (curNode.state[0]-1,curNode.state[1]+1) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0]-1,curNode.state[1]+1)] = self.Node((curNode.state[0]-1,curNode.state[1]+1),curNode)
			nodes.append(('NE',self.nodeDict[(curNode.state[0]-1,curNode.state[1]+1)],curNode))
		if self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]+2] == 0:
			if (curNode.state[0],curNode.state[1]+1) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0],curNode.state[1]+1)] = self.Node((curNode.state[0],curNode.state[1]+1),curNode)
			nodes.append(('L',self.nodeDict[(curNode.state[0],curNode.state[1]+1)],curNode))
		if self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]+2] == 0:
			if (curNode.state[0]+1,curNode.state[1]+1) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0]+1,curNode.state[1]+1)] = self.Node((curNode.state[0]+1,curNode.state[1]+1),curNode)
			nodes.append(('SE',self.nodeDict[(curNode.state[0]+1,curNode.state[1]+1)],curNode))
		if self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]+1] == 0:
			if (curNode.state[0]+1,curNode.state[1]) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0]+1,curNode.state[1])] = self.Node((curNode.state[0]+1,curNode.state[1]),curNode)
			nodes.append(('S',self.nodeDict[(curNode.state[0]+1,curNode.state[1])],curNode))
		if self.prob.mazeBelief[curNode.state[0]+2][curNode.state[1]] == 0:
			if (curNode.state[0]+1,curNode.state[1]-1) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0]+1,curNode.state[1]-1)] = self.Node((curNode.state[0]+1,curNode.state[1]-1),curNode)
			nodes.append(('SO',self.nodeDict[(curNode.state[0]+1,curNode.state[1]-1)],curNode))
		if self.prob.mazeBelief[curNode.state[0]+1][curNode.state[1]] == 0:
			if (curNode.state[0],curNode.state[1]-1) not in self.nodeDict.keys():
				self.nodeDict[(curNode.state[0],curNode.state[1]-1)] = self.Node((curNode.state[0],curNode.state[1]-1),curNode)
			nodes.append(('O',self.nodeDict[(curNode.state[0],curNode.state[1]-1)],curNode))
		return nodes
