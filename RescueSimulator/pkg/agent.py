from agentExp import AgentExplorer
from agentResc import AgentResc
from problem import Problem
from stateMesh import StateMesh

class Agent():
    def __init__(self,model,configDict):
        #Lista de agentes
        self.prob = Problem()
        self.stateMesh = StateMesh()
        self.agentExp = AgentExplorer(model,configDict,self.prob,self.stateMesh)
        self.agentResc = AgentResc(model,configDict,self.prob,self.stateMesh)
        self.agent = self.agentExp

    def execute(self):
        state = self.agent.deliberate()

        if state == 0:
            self.agentResc.setVictims(self.agentExp.getVictims())
            
            self.agent = self.agentResc

        return state
