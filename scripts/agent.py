import matlab.engine
import os
import datetime
import threading
import random
import termcolor
import numpy as np
from typing import List


class Agent:
    _thread: threading.Thread
    id: int
    P: float
    I: float
    D: float

    def __init__(self, id: int, randomInit: bool = False, p: float = 1.0, i: float = 1.0, d: float = 1.0):
        self.id = id
        self._thread = None

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
        print(self)
        pass

    def finish(self):
        self._thread.join()

    def __str__(self):
        return termcolor.colored(f"| ID: {self.id} | Thread: {self._thread}", 'blue')