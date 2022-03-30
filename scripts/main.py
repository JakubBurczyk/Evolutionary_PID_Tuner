import random

from ea_pid_tuner import *
from gui import *

if __name__ == '__main__':
    tuner = PidTuner(agentCount=5, itCount=2)

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
        data = tuner.getIteration() #CRITICAL!!! DO NOT REMOVE
        #testValue = random.random()
        testValue = spinbox_one.value

        if data is not None:
            dispIterCnt = data
            print(colored(" " + str(datetime.datetime.now()) + " |  " + str(data), 'red'))
            pass

        pass