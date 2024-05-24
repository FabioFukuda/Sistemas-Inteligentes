from agentExp import AgentExplorer
from agentResc import AgentResc
from problem import Problem
from stateMesh import StateMesh

class Agent():
    def __init__(self,model,configDict):
        self.prob = Problem()
        self.stateMesh = StateMesh()
        #Lista de agentes
        self.agentExp = AgentExplorer(model,configDict,self.prob,self.stateMesh)
        self.agentResc = AgentResc(model,configDict,self.prob,self.stateMesh)
        self.agent = self.agentExp
        self.curAgent = 'exp'

    def execute(self):
        state = self.agent.deliberate()

        if state == 0 and self.curAgent=='exp':
            self.agentResc.setVictims(self.agentExp.getVictims())
            if(self.agentResc.elaboratePlan() == 1):
                self.agentResc.deliberate()
                self.agent = self.agentResc
                self.curAgent = 'resc'
            else:
                return 0
        return state
