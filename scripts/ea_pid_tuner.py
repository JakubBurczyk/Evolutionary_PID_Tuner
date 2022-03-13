import threading

from agent import *


class PidTuner:
    # threadList: List[threading.Thread]
    _running: bool
    _finished: bool
    _tunerThread: threading.Thread

    def __init__(self,agentCount=1, itCount=1):
        self._agents = [Agent(i, randomInit=True) for i in range(agentCount)]
        self._running = False
        self._finished = True
        self._iterations = itCount
        self._iterationCounter = 0
        self._tunerThread = None
        pass

    def start(self):
        print("Starting tuner")
        self._finished = True
        self._tunerThread = threading.Thread(target=self.runIterLoop)
        self._tunerThread.setDaemon(True)
        self._tunerThread.start()
        pass

    def runIterLoop(self):
        i = 0
        while i < self._iterations:
            if self._finished is True:
                #print(f"Iter loop {self._iterationCounter}")
                self.runStep()
                self._iterationCounter += 1
                i += 1
                """HERE WE WILL RUN ALGO"""
                self.runAlgo()
            else:
                continue
        self._finished = False
        pass

    def runStep(self) -> None:
        """
        Run each agent's simulation thread.
        """
        #print("Sim step")
        self._running = True
        self._finished = False
        ''' Start each thread'''
        for agent in self._agents:
            agent.start()

        '''Finish joins each agent's thread, crucial to run in separate loop!'''
        for agent in self._agents:
            agent.finish()

        self._running = False

    def runAlgo(self):
        """
        @TODO: Implement algorithm
        :return:
        """
        pass

    def updateState(self):
        """
        Update running and finished state of tuner iteration.

        :return:
        """
        prev_running_state = self._running
        self._running = any([agent.isRunning for agent in self._agents])

        if prev_running_state is True and self._running is False:
            self._finished = True
            pass
        pass

    def getIteration(self):
        """
        @TODO: FILL
        :return:
        """
        if not self._running and not self._finished:
            self._finished = True
            return self._iterationCounter
        else:
            return None

    @property
    def isRunning(self) -> bool:
        """
        Check whether an iteration is running
        :return:
        """
        return self._running

    @property
    def hasFinished(self) -> bool:
        """
        Returns whether the tuner has finished an iteration.
        Changes state of Finished to False.
        WARNING: HAS TO BE INVOKED BEFORE NEXT runStep() call.

        :return: boolean True if an iteration was finished
        """

        return self._finished
