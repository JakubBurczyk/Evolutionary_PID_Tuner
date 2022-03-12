from agent import *


class PidTuner:
    # threadList: List[threading.Thread]

    def __init__(self, agentCount=1):
        self._agents = [Agent(i, randomInit=True) for i in range(agentCount)]
        pass

    def runStep(self) -> None:
        """
        Run each agent's simulation thread.
        """
        ''' Start each thread'''
        for agent in self._agents:
            agent.start()

        '''Finish joins each agent's thread, crucial to run in separate loop!'''
        for agent in self._agents:
            agent.finish()
