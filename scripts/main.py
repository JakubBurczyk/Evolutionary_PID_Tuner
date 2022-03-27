import random

from ea_pid_tuner import *
from gui import *

if __name__ == '__main__':
    tuner = PidTuner(agentCount=2, itCount=5)

    gui = GUI()
    gui.addWindow(name="mainWindow", file="GUI_v1.ui")
    gui.openWindow(name="mainWindow")

    testValue = 0
    dispIterCnt = 0
    gui.windows["mainWindow"].addButton("pushButton", lambda: tuner.start())
    gui.windows["mainWindow"].addButton("pushButton_2", lambda: gui.windows["mainWindow"].lcds["lcdNumber"].display(random.random()))
    gui.windows["mainWindow"].addLCD("lcdNumber")
    gui.windows["mainWindow"].lcds["lcdNumber"].setCallback(lambda: testValue)
    gui.windows["mainWindow"].addSpinBox("doubleSpinBox", double=True)
    #tuner.start()

    while gui.isOpened:
        gui.update()
        data = tuner.getIteration() #CRITICAL!!! DO NOT REMOVE
        #testValue = random.random()
        testValue = gui.windows["mainWindow"].spinboxes["doubleSpinBox"].value

        if data is not None:
            dispIterCnt = data
            print(colored(" " + str(datetime.datetime.now()) + " |  " + str(data), 'red'))
            pass
        
        pass