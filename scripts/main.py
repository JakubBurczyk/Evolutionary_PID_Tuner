from ea_pid_tuner import *
from gui import *

if __name__ == '__main__':
    tuner = PidTuner(10)
    tuner.runStep()

    gui = GUI()
    gui.addWindow("mainWindow", "GUI_v1.ui")
    gui.openWindow("mainWindow")

    gui.start()
