from agent import *


class PidTuner:
    # threadList: List[threading.Thread]

    def __init__(self, agentCount=1):
        self._agents = [Agent(i, randomInit=True) for i in range(agentCount)]
        pass

    def runStep(self):
        # threadList: List[threading.Thread] = []

        for agent in self._agents:
            agent.start()

        for agent in self._agents:
            agent.finish()
