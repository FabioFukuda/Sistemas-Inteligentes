from state import State

class DFS:
	class Node:
		def __init__(self,state,parent = None):
			self.parent = None
			self.state = state
			
	def __init__(self,prob = None):
		self.prob = prob
		self.stack = []
		self.current = None
		
	def dfs(self,state):
		if state != self.current.state:
			self.current = self.current.parent
 			return self.stack.pop()
			
		curNode = self.Node(state)
		nodes = self.createPosNodes(curNode)
		
		if nodes.empty():
			self.current = self.current.parent
			self.stack.pop()
			
		self.stack.append(nodes)
		return self.stack.pop()
		
	def createPosNodes(self,state):
		nodes = []	
		if self.prob.mazeBelief[state.row][state.col] == 0:
			nodes.append(self.Node(State(state.row-1,state.col-1),state))
		if self.prob.mazeBelief[state.row][state.col+1] == 0:
			nodes.append(self.Node(State(state.row-1,state.col),state))
		if self.prob.mazeBelief[state.row][state.col+2] == 0:
			nodes.append(self.Node(State(state.row-1,state.col+1),state))
		if self.prob.mazeBelief[state.row+1][state.col+2] == 0:
			nodes.append(self.Node(State(state.row,state.col+1),state))
		if self.prob.mazeBelief[state.row+2][state.col+2] == 0:
			nodes.append(self.Node(State(state.row+1,state.col+1),state))
		if self.prob.mazeBelief[state.row+2][state.col+1] == 0:
			nodes.append(self.Node(State(state.row+1,state.col),state))
		if self.prob.mazeBelief[state.row+2][state.col] == 0:
			nodes.append(self.Node(State(state.row+1,state.col-1),state))
		if self.prob.mazeBelief[state.row+1][state.col] == 0:
			nodes.append(self.Node(State(state.row,state.col-1),state))
		return nodes
	
		
	
