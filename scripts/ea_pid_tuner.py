from agent import *


class PidTuner:

    def __init__(self, agentCount=1):
        self._agents = [Agent(i, randomInit=True) for i in range(agentCount)]
        pass

    def runStep(self):
        threadList = list(threading.Thread)
        for agent in self._agents:
            agent.run(threadList)

