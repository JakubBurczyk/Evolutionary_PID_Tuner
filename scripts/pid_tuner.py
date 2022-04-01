import threading

from agent import *
from bee_algorithm import *


class PidTuner:
    _running: bool
    _finishedIteration: bool
    _tunerThread: threading.Thread or None
    _result: IterationResult or None

    def __init__(self, agentCount=1, itCount=1):
        self._finishedAlgo = False
        self._finishedIteration = True
        self._iterations = itCount
        self._iterationCounter = 0
        self._tunerThread = None
        self._result = None
        self._ba = BeeAlgo(agentCount)
        pass

    def __del__(self):
        print("Deleting pid tuner")
        del self._ba

    def start(self):
        print("Starting tuner")
        self._finishedAlgo = False
        self._finishedIteration = True
        self._tunerThread = threading.Thread(target=self.runIterLoop)
        self._tunerThread.setDaemon(True)
        self._tunerThread.start()
        pass

    def runIterLoop(self):
        i = 0
        while i < self._iterations:
            if self._finishedIteration is True:

                print(f"Iter loop {self._iterationCounter}")
                self._finishedIteration = False
                self.runAlgo()  # THIS IS BLOCKING
                self._iterationCounter += 1
                i += 1
            else:
                continue

        self._finishedAlgo = True
        pass

    def runAlgo(self):
        """
        @TODO: Implement algorithm
        :return:
        """
        self._running = True
        self._result = self._ba.run() #BLOCKING FUNCTION
        self._running = False
        pass

    def getIterationResult(self) -> IterationResult or None:
        """
        @TODO: FILL
        :return:
        """
        if self._finishedIteration is False and self._running is False and self._iterationCounter != 0:
            print("RETURNING ITERATION RESULTS")
            self._finishedIteration = True
            return self._result
        else:
            return None

    @property
    def hasFinishedIteration(self) -> bool:
        """
        Returns whether the tuner has finished an iteration.
        Changes state of Finished to False.
        WARNING: HAS TO BE INVOKED BEFORE NEXT runStep() call.

        :return: boolean True if an iteration was finished
        """

        return self._finishedIteration
