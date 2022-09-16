from agentExp import AgentExplorer
from agentResc import AgentResc

class Agent():
    def __init__(self,model,configDict):
        #Lista de agentes
        self.agentExp = AgentExplorer(model,configDict)
        #self.agentResc = AgentResc(model,configDict)
        self.agent = self.agentExp

    def execute(self):
        state = self.agent.deliberate()

        if state == 0:
            self.agentResc.setVictims(self.agentExp.getVictims())
            self.agent = self.agentResc

        return state
