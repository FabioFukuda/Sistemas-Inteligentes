from agentExp import AgentExplorer

class Agent():
    def __init__(self,model,configDict):
        #Lista de agentes
        self.agent = AgentExplorer(model,configDict)

    def execute(self):
        state = self.agent.deliberate()
        return state
