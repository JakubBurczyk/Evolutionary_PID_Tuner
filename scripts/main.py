import random

import matplotlib.pyplot as plt

from pid_tuner import *
from gui import *
import pickle
import dill


class EvolutionalTuner:
    addWidgets: Callable

    iterationResult: IterationResult

    mainWin: Window
    button_tunerStart: widgets.Button
    spinbox_agentCount: widgets.SpinBox
    spinbox_iterations: widgets.SpinBox
    lcd_iteration: widgets.LCD

    def __init__(self, mainUiFile):
        self._gui = GUI()

        self.mainWin = self._gui.addWindow(name="mainWindow", file=mainUiFile)
        self._gui.openWindow(name="mainWindow")

        self._tuner = None
        self.iterationResult = IterationResult()

        self.addWidgets()
        self.best_costs = []

        pass

    def addWidgets(self) -> None:
        """
        Adding widgets
        :return:
        """

        '''BUTTONS'''
        self.button_tunerStart = self.mainWin.addButton("pushButton_startTuner", self.start_tuner)
        #self.button_randomDisp = mainWin.addButton("pushButton_2",lambda: gui.windows["mainWindow"].lcds["lcdNumber"].display(random.random()))
        self.button_restart = self.mainWin.addButton("pushButton_restartTuner", self.restart)
        '''SPINBOXES'''
        self.spinbox_agentCount = self.mainWin.addSpinBox("spinBox_agentCount", double=False)
        self.spinbox_iterations = self.mainWin.addSpinBox("spinBox_iterations", double=False)
        self.spinbox_mean = self.mainWin.addSpinBox("spinBox_mean", double=False)
        self.spinbox_std = self.mainWin.addSpinBox("spinBox_std", double=False)
        self.spinbox_search = self.mainWin.addSpinBox("doubleSpinBox_search", double=True)

        '''LCD DISPLAYS'''
        self.lcd_iteration = self.mainWin.addLCD("lcdNumber_iteration")
        self.lcd_iteration.setCallback(lambda: self.iterationResult.iteration)

        self.lcd_cost = self.mainWin.addLCD("lcdNumber_cost")
        self.lcd_P = self.mainWin.addLCD("lcdNumber_P")
        self.lcd_I = self.mainWin.addLCD("lcdNumber_I")
        self.lcd_D = self.mainWin.addLCD("lcdNumber_D")

        '''PIXMAPS'''
        self.pixmap_costs = self.mainWin.addPixMap("label_pixmap_costs","costs.jpg")
        self.pixmap_response = self.mainWin.addPixMap("label_pixmap_response", "response.jpg")

        '''ACTIONS'''
        self.mainWin.addAction_("action_save", self.save)
        self.mainWin.addAction_("action_load", self.load)

        pass

    def run(self) -> None:
        """
        Main loop

        :return: None
        """

        while self._gui.isOpened:
            self._gui.update()

            if self._tuner is not None:

                iterationResult = self._tuner.getIterationResult()  # CRITICAL!!! DO NOT REMOVE

                if iterationResult is not None:
                    self.iterationResult = iterationResult
                    self.lcd_iteration.display(self.iterationResult.iteration)
                    self.lcd_cost.display(self.iterationResult.bestAgent.cost)
                    self.lcd_P.display(self.iterationResult.bestAgent.P)
                    self.lcd_I.display(self.iterationResult.bestAgent.I)
                    self.lcd_D.display(self.iterationResult.bestAgent.D)

                    if self.iterationResult.finished:
                        self.button_tunerStart.enable()
                        self.button_restart.enable()

                    print(colored(" " + str(datetime.datetime.now()) +
                                  " | iteration:  " + str(self.iterationResult.iteration) +
                                  " | start iteration:  " + str(self.iterationResult.startIteration) +
                                  " | end iteration:  " + str(self.iterationResult.endIteration) +
                                  " | finished: " + str(self.iterationResult.finished) +
                                  " | Lowest cost: " + str(self.iterationResult.cost),
                                  'red'))

                    plt.plot(self.iterationResult.bestAgent.t, self.iterationResult.bestAgent.response)
                    plt.title(f"Iteration: {self.iterationResult.iteration}")
                    plt.savefig('response.jpg')
                    plt.show()

                    self.best_costs.append(self.iterationResult.cost)
                    print(colored(self.best_costs, 'magenta'))

                    if self.iterationResult.endIteration == len(self.best_costs):
                        print("HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        plt.plot(range(len(self.best_costs)), self.best_costs)
                        plt.title("Best values of cost function per iteration")
                        plt.savefig('costs.jpg')
                        plt.show()


        pass

    def start_tuner(self):
        ba_params: BeeAlgoParams
        if self._tuner is None:
            self.button_restart.disable()
            self.button_tunerStart.disable()
            self.spinbox_mean.disable()
            self.spinbox_std.disable()
            self.spinbox_agentCount.disable()
            self.spinbox_search.disable()
            #self._gui.update()
            ba_params = BeeAlgoParams()
            ba_params.mean = self.spinbox_mean.value
            ba_params.std = self.spinbox_std.value
            ba_params.search = self.spinbox_search.value

            self._tuner = PidTuner(agentCount=self.spinbox_agentCount.value, itCount=self.spinbox_iterations.value, ba_params=ba_params)

        if self._tuner.finished:
            self.button_tunerStart.disable()
            self.button_restart.disable()
            self._tuner._iterations = self.spinbox_iterations.value
            self._tuner.start()
        pass

    def save(self):
        print(colored("Attempting save", "red"))
        print(dill.detect.trace(True))
        print(dill.detect.baditems(self._tuner))
        with open(f'iter_{self.iterationResult.iteration}_{datetime.datetime.strftime(datetime.datetime.now(), "%m-%d-%Y_T+%H-%M-%S")}', 'wb') as output_file:
            pickle.dump(self._tuner, output_file, pickle.HIGHEST_PROTOCOL)
            pass
        pass

    def load(self):
        print(colored("Attempting load", "red"))
        filePath = QFileDialog.getOpenFileName(self.mainWin, 'Open a file', '', 'All Files (*.*)')
        if filePath != ('', ''):
            with open(f'iter_{self.iterationResult.iteration}_{datetime.datetime.strftime(datetime.datetime.now(), "%m-%d-%Y_T+%H-%M-%S")}', 'wb') as input_file:
                print(colored(filePath[0], "blue"))
                self._tuner = pickle.load(input_file)
                pass
        pass

    def restart(self):
        self._tuner = None
        self.iterationResult = IterationResult()
        self.spinbox_mean.enable()
        self.spinbox_std.enable()
        self.spinbox_search.enable()
        self.spinbox_agentCount.enable()
        self.best_costs = []

        self.lcd_cost.display(0)
        self.lcd_P.display(0)
        self.lcd_I.display(0)
        self.lcd_D.display(0)
        try:
            os.remove("costs.jpg")
            os.remove("response.jpg")
        except:
            pass


if __name__ == '__main__':
    try:
        os.remove("costs.jpg")
        os.remove("response.jpg")
    except:
        pass

    evolutionalTunerApp = EvolutionalTuner("GUI_v1.ui")
    evolutionalTunerApp.run()

    """
    data: IterationResult


    tuner = PidTuner(agentCount=15, itCount=2)

    gui = GUI()
    mainWin = gui.addWindow(name="mainWindow", file="GUI_v1.ui")
    gui.openWindow(name="mainWindow")

    testValue = 0
    dispIterCnt = 0

    button_tunerStart = mainWin.addButton("pushButton", lambda: tuner.start())
    button_randomDisp = mainWin.addButton("pushButton_2", lambda: gui.windows["mainWindow"].lcds["lcdNumber"].display(random.random()))

    lcd_one = mainWin.addLCD("lcdNumber")
    lcd_one.setCallback(lambda: testValue)

    spinbox_one = mainWin.addSpinBox("doubleSpinBox", double=True)
    #tuner.start()

    while gui.isOpened:
        gui.update()
        data = tuner.getIterationResult() #CRITICAL!!! DO NOT REMOVE
        #testValue = random.random()
        testValue = spinbox_one.value

        if data is not None:
            dispIterCnt = data
            print(colored(" " + str(datetime.datetime.now()) + " |  " + str(data.bestAgent.cost) , 'red'))

            pass
        else:
            pass

        pass"""