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

    def __init__(self):
        self._gui = GUI()

        self.mainWin = self._gui.addWindow(name="mainWindow", file="GUI_v1.ui")
        self._gui.openWindow(name="mainWindow")

        self._tuner = None
        #self.button_randomDisp = None
        self.addWidgets()

        pass

    def addWidgets(self) -> None:
        """
        Adding widgets
        :return:
        """

        '''BUTTONS'''
        self.button_tunerStart = self.mainWin.addButton("pushButton_startTuner", self.start_tuner)
        #self.button_randomDisp = mainWin.addButton("pushButton_2",lambda: gui.windows["mainWindow"].lcds["lcdNumber"].display(random.random()))

        '''SPINBOXES'''
        self.spinbox_agentCount = self.mainWin.addSpinBox("spinBox_agentCount", double=False)
        self.spinbox_iterations = self.mainWin.addSpinBox("spinBox_iterations", double=False)

        '''LCD DISPLAYS'''
        self.lcd_iteration = self.mainWin.addLCD("lcdNumber_iteration")

        pass

    def run(self) -> None:
        """
        Main loop

        :return: None
        """

        while self._gui.isOpened:
            self._gui.update()

            if self._tuner is not None:

                self.iterationResult = self._tuner.getIterationResult()  # CRITICAL!!! DO NOT REMOVE

                if self.iterationResult is not None:
                    self.lcd_iteration.display(self.iterationResult.iteration)

                    if self.iterationResult.finished:
                        self.button_tunerStart.enable()
                        self.save()

                    print(colored(" " + str(datetime.datetime.now()) +
                                  " | iteration:  " + str(self.iterationResult.iteration) +
                                  " | start iteration:  " + str(self.iterationResult.startIteration) +
                                  " | end iteration:  " + str(self.iterationResult.endIteration) +
                                  " | finished: " + str(self.iterationResult.finished) +
                                  " | Lowest cost: " + str(self.iterationResult.cost),
                                  'red'))

                    plt.plot(self.iterationResult.bestAgent.t, self.iterationResult.bestAgent.response)
                    plt.show()
                    pass

        pass

    def start_tuner(self):
        if self._tuner is None:
            self.button_tunerStart.disable()
            #self._gui.update()
            self._tuner = PidTuner(agentCount=self.spinbox_agentCount.value, itCount=self.spinbox_iterations.value)

        if self._tuner.finished:
            self.button_tunerStart.disable()
            self._tuner._iterations = self.spinbox_iterations.value
            self._tuner.start()
        pass

    def save(self):
        with open(f'iter_{self.iterationResult.iteration}_{datetime.datetime.strftime(datetime.datetime.now(),"%m-%d-%Y_T+%H-%M-%S")}','wb') as output_file:
            print(dill.detect.trace(True))
            print(dill.detect.baditems(self))
            #pickle.dump(self,output_file,pickle.HIGHEST_PROTOCOL)
            pass
        pass


if __name__ == '__main__':
    evolutionalTunerApp = EvolutionalTuner()
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