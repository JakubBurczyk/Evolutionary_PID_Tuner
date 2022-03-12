from ea_pid_tuner import *
from gui import *

if __name__ == '__main__':
    tuner = PidTuner(10)
    tuner.runStep()

    gui = GUI()
    gui.addWindow(name="mainWindow", file="GUI_v1.ui")
    gui.openWindow(name="mainWindow")

    gui.start()
