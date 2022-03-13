from ea_pid_tuner import *
from gui import *

if __name__ == '__main__':
    tuner = PidTuner(1,5)

    gui = GUI()
    gui.addWindow(name="mainWindow", file="GUI_v1.ui")
    gui.openWindow(name="mainWindow")

    gui.windows["mainWindow"].addButton("pushButton", lambda: gui.windows["mainWindow"].say(gui.windows["mainWindow"].buttons["pushButton"].name))
    print(gui.windows["mainWindow"].buttons["pushButton"].widget)

    tuner.start()
    while gui.isOpened:
        gui.update()
        data = tuner.getIteration()
        if data is not None:
            print(colored(" " + str(datetime.datetime.now()) + " |  "+ str(data),'red'))

        pass
