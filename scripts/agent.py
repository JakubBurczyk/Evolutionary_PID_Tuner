import matlab.engine
import os
import datetime
import threading
import random
import pickle
import dill
import matplotlib.pyplot as plt
import numpy
from termcolor import colored
import numpy as np
from typing import List
import time


class Agent:
    _thread: threading.Thread or None
    _eng: matlab.engine
    _functionName: str
    nargoutCount: int
    id: int
    P: float
    I: float
    D: float
    cost: float

    def __init__(self, eng: matlab.engine, functionName: str, nargoutCount:int , randomInit: bool = False, p: float = 1.0, i: float = 1.0, d: float = 1.0, mean = 10, std = 10):
        self._eng = eng
        self._functionName = functionName
        self.nargoutCount = nargoutCount

        self._thread = None
        self._isElite = False

        self.P = 1
        self.I = 1
        self.D = 1
        self.cost = np.inf
        self.t = []
        self.response = []

        self.mean = mean
        self.std_deviation = std
        if randomInit:
            self.randomInit()
        else:
            if isinstance(p, np.ndarray):
                self.P = p.tolist()[0]
            else:
                self.P = p

            if isinstance(i, np.ndarray):
                self.I = i.tolist()[0]
            else:
                self.I = i

            if isinstance(d, np.ndarray):
                self.D = d.tolist()[0]
            else:
                self.D = d
            #self.P = p
            #self.I = i
            #self.D = d
        pass

    def randomInit(self):

        self.P = max(0, np.random.normal(loc=self.mean, scale=self.std_deviation, size=1))
        self.I = max(0, np.random.normal(loc=self.mean, scale=self.std_deviation, size=1))
        self.D = max(0, np.random.normal(loc=self.mean, scale=self.std_deviation, size=1))

    def start(self, threadList: list[threading.Thread] = None):
        self._thread = threading.Thread(target=self.run)
        self._thread.setDaemon(True)

        # threadList.append(self._thread)

        self._thread.start()
        pass

    def run(self):

        #print(f"Thread[{self._thread}] START: ", datetime.datetime.now())
        try:
            self.cost, self.t, self.response = self._eng.eval(f"{self._functionName}({self.P},{self.I},{self.D})", nargout=self.nargoutCount)
        except Exception as e:
            print(colored("AGENT ENCOUNTERED SIMULATION ERROR, DISMISSING HIS RESULT, Caused by:" + str(e)))
            self.cost = np.inf
        #print(f"Thread[{self._thread}] FINISH: ", datetime.datetime.now())
        pass

    def finish(self) -> None:
        """
        Join agent's thread.
        WARNING: This blocks the invoking thread until this thread is finished.

        :return: None
        """
        self._thread.join()

    @property
    def isRunning(self) -> bool:
        """
        Check if agent's thread is running the simulation

        :return: If thread is running returns True, else returns False
        """
        return self._thread.is_alive()

    def __str__(self):
        return colored(f"Bee |Thread: {self._thread} | P: {self.P} | I: {self.I} | D: {self.D} | Cost: {self.cost}", 'yellow')


if __name__ == '__main__':
    eng = matlab.engine.start_matlab()
    agentCount = 3

    agents = [Agent(eng=eng, functionName="test", nargoutCount=4, randomInit=True) for i in range(agentCount)]
    for agent in agents:
        agent._thread = None
    print(colored("Attempting save", "red"))
    print(dill.detect.trace(True))
    print(dill.detect.baditems(agents))
    with open(
            f'agents_{datetime.datetime.strftime(datetime.datetime.now(), "%m-%d-%Y_T+%H-%M-%S")}','wb') as output_file:
        pickle.dump(agents, output_file, pickle.HIGHEST_PROTOCOL)
        pass
    pass