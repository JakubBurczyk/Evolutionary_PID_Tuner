import matlab.engine
import os
import datetime
import threading
import random

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

    def __init__(self, eng: matlab.engine, functionName: str, nargoutCount:int , randomInit: bool = False, p: float = 1.0, i: float = 1.0, d: float = 1.0):
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

        if randomInit:
            self.randomInit()
        else:
            self.P = p
            self.I = i
            self.D = d
        pass

    def randomInit(self, mean: float = 1, std_deviation: float = 1):
        self.P = np.random.normal(loc=mean, scale=std_deviation, size=1)
        self.I = np.random.normal(loc=mean, scale=std_deviation, size=1)
        self.D = np.random.normal(loc=mean, scale=std_deviation, size=1)

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
        WARNING: This blocks the invoking thread untill this thread is finished.

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
