import threading

from agent import *
from bee_algorithm import *


@dataclass
class IterationResult(BeeIterationResult):
    iteration: int = 0
    startIteration: int = 0
    endIteration: int = 0
    finished: bool = False


class PidTuner:
    _running: bool = True
    _finishedIteration: bool
    _tunerThread: threading.Thread or None
    _result: IterationResult or None
    _startIteration: int = 0
    _endIteration: int = 0

    def __init__(self, agentCount=1, itCount=1, ba_params:BeeAlgoParams=BeeAlgoParams()):
        self._finishedAlgo = True
        self._finishedIteration = True
        self._iterations = itCount
        self._iterationCounter = 0
        self._tunerThread = None
        self._result = IterationResult()
        self._ba_params = ba_params
        self._ba = None
        self._agentCount = agentCount
        pass

    def __del__(self):
        print("Deleting pid tuner")
        print(type, self._ba)
        del self._ba

    def start(self):
        print("Starting tuner")

        self._finishedAlgo = False
        self._finishedIteration = True
        self._startIteration = self._iterationCounter
        self._endIteration = self._iterationCounter + self._iterations

        self._tunerThread = threading.Thread(target=self.runIterLoop)
        self._tunerThread.setDaemon(True)
        self._tunerThread.start()
        pass

    def runIterLoop(self):
        i = 0

        while i < self._iterations:
            if self._finishedIteration is True:
                self._iterationCounter += 1
                print(f"Iter loop {self._iterationCounter}")

                self._finishedIteration = False
                self.runAlgo()  # THIS IS BLOCKING

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
        if self._ba is None:
            self._ba = BeeAlgo(agentCount=self._agentCount,params=self._ba_params)

        self._running = True
        self._result = IterationResult(self._ba.run()) #BLOCKING FUNCTION
        self._running = False

        self._result.iteration = self._iterationCounter
        self._result.startIteration = self._startIteration
        self._result.endIteration = self._endIteration

        if self._result.iteration == self._result.endIteration:
            self._result.finished = True
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

    @property
    def finished(self) -> bool:
        return self._finishedAlgo
