from agent import *
import matlab.engine
import os
from termcolor import colored
import atexit

class BeeAlgo:

    def __init__(self, agentCount=1):

        self._running = True
        self._finished = False

        print(colored("Starting BeeAlgo matlab engine: " + str(datetime.datetime.now()) + "...","green"))
        self.matlabScriptsPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "../"*2,"matlab"))
        print(colored("Setting scripts path:" + self.matlabScriptsPath,"yellow"))
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(self.matlabScriptsPath)

        print(colored("STARTED BeeAlgo matlab engine: " + str(datetime.datetime.now()),"red"))

        self.nargoutCount = 1
        self.functionName = "testFunction"

        self._agents = [Agent(eng=self.eng ,functionName=self.functionName, nargoutCount=self.nargoutCount, randomInit=True) for i in range(agentCount)]
        atexit.register(self.kill)
        pass

    def kill(self):
        print(colored("Killing BA matlab engine"),"red")
        self.eng.exit()

    def run(self):
        self.runAgents()
        self.selectElites()

    def selectElites(self):
        self._agents.sort(key=lambda ag: ag.cost, reverse=False)

        for agent in self._agents:
            print(colored(agent.cost, "magenta"))
        pass

    def runAgents(self) -> None:
        """
        Run each agent's simulation thread.
        """
        print(colored("BeeAlgo running agents","blue"))
        self._running = True
        self._finished = False
        ''' Start each thread'''
        for agent in self._agents:
            agent.start()

        '''Finish joins each agent's thread, crucial to run in separate loop!'''
        for agent in self._agents:
            agent.finish()

        self._running = False

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


