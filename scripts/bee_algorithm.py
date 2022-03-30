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

        print(colored("STARTED BeeAlgo matlab engine: " + str(datetime.datetime.now()),"blue"))

        self.nargoutCount = 1
        self.functionName = "testFunction"

        self._agents = [Agent(eng=self.eng, functionName=self.functionName, nargoutCount=self.nargoutCount, randomInit=True) for i in range(agentCount)]
        atexit.register(self.kill)

        self.agentCount = agentCount
        self._eliteNumber = 0
        self._goodNumber = 0
        self.setBeesNumber()

        self._eliteBees = []
        self._goodBees = []

        self._searchArea = 1
        self._eliteAreaBeesNumber = 0
        self._goodAreaBeesNumber = 0
        self.setAreaBeesNumber()

        #self._areaBees = []

        pass

    def setBeesNumber(self):
        self._eliteNumber = max(1, int(0.2 * self.agentCount))
        if self.agentCount == 1:
            self._goodNumber = 0
        else:
            self._goodNumber = max(1, int(0.3 * self.agentCount))

    def setAreaBeesNumber(self):
        self._eliteAreaBeesNumber = int(0.4 * self.agentCount)
        self._goodAreaBeesNumber = int(0.2 * self.agentCount)

    def kill(self):
        print(colored("Killing BA matlab engine","red"))
        self.eng.exit()

    def run(self):
        self.runAgents(self._agents)  # evaluation
        self.selectBestBees()
        allAreas = self.recruitNewBees()
        temp = sum(allAreas.values(), [])
        self.runAgents(temp)
        self.selectNewPopulation(allAreas)

    def selectBestBees(self):
        self._agents.sort(key=lambda ag: ag.cost, reverse=False)

        self._eliteBees = self._agents[:self._eliteNumber]
        self._goodBees = self._agents[self._eliteNumber:self._eliteNumber+self._goodNumber]

        for agent in self._agents:
            print(colored(agent.cost, "magenta"))
        pass

    def recruitNewBees(self):
        allAreas = {}
        self.createNewArea(allAreas, self._eliteBees, self._eliteAreaBeesNumber)
        self.createNewArea(allAreas, self._goodBees, self._goodAreaBeesNumber)
        return allAreas

    def createNewArea(self, allAreas, bees, number):
        for leadBee in bees:
            singleArea = []
            for i in range(number):
                new_p = np.random.uniform(leadBee.P - self._searchArea/2, leadBee.P + self._searchArea/2)
                new_i = np.random.uniform(leadBee.I - self._searchArea/2, leadBee.I + self._searchArea/2)
                new_d = np.random.uniform(leadBee.D - self._searchArea/2, leadBee.D + self._searchArea/2)
                newBee = Agent(eng=self.eng, functionName=self.functionName, nargoutCount=self.nargoutCount, randomInit=False, p=new_p, i=new_i, d=new_d)
                singleArea.append(newBee)
            allAreas[leadBee] = singleArea

    def selectNewPopulation(self, allAreas) -> None:
        self._agents.clear()

        for leadBee, bees in allAreas.items():
            bees.append(leadBee)
            bees.sort(key=lambda ag: ag.cost, reverse=False)
            self._agents.append(bees[0])

        while len(self._agents) < self.agentCount:
            self._agents.append(
                Agent(eng=self.eng, functionName=self.functionName, nargoutCount=self.nargoutCount, randomInit=True))

    def runAgents(self, agents: List[Agent]) -> None:
        """
        Run each agent's simulation thread.
        """
        print(colored("BeeAlgo running agents", "blue"))
        self._running = True
        self._finished = False
        ''' Start each thread'''
        for agent in agents:
            agent.start()

        '''Finish joins each agent's thread, crucial to run in separate loop!'''
        for agent in agents:
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


