import threading


class AgentFramework:
    def __init__(self):
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)

    def start_all(self):
        threads = []
        for agent in self.agents:
            t = threading.Thread(target=agent.run)
            t.daemon = True
            t.start()
            threads.append(t)
        return threads