from ea_pid_tuner import *
from gui import *

if __name__ == '__main__':
    tuner = PidTuner(1,5)

    gui = GUI()
    gui.addWindow(name="mainWindow", file="GUI_v1.ui")
    gui.openWindow(name="mainWindow")

    tuner.start()
    while gui.isOpened:
        gui.update()
        data = tuner.getData()
        if data is not None:
            print(" " + str(datetime.datetime.now()) + " |  "+ str(data))
        pass
