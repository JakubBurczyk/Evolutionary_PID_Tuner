from PyQt5.QtWidgets import *
from typing import List, Dict
from window import *
import os


class GUI:
    def __init__(self):
        """
        Class describing  graphical user interface via Qt.
        """
        self.uisDir = os.path.abspath(os.path.join(os.path.realpath(__file__), "../"*2, "uis"))
        self.windows: Dict[str, Window] = {}
        self.app = QtWidgets.QApplication([])
        print(colored("Initializing GUI",'green'))
        pass

    def addWindow(self, name: str, file: str) -> None:
        """
        :param name: Name of the window in GUI dictionary
        :param file: Name of the .ui file describing layout
        """
        if name not in self.windows.keys():
            self.windows[name] = Window(name, os.path.join(self.uisDir, file))
        else:
            raise AttributeError("That window already exists")
        pass

    def start(self) -> None:
        """
        WARNING: THIS IS A BLOCKING METHOD, USE update() METHOD IF EXTERNAL LOOP IS NEEDED.

        Start the GUI with opened windows. If no window is opened before the start() method is invoked,
        the application will be terminated.

        :return: None
        """
        while self.isOpened:
            self.update()
        pass

    def update(self) -> None:
        """
        Processing of QtApplication Events and updating each currently opened window.

        :return: None
        """
        # processing QtApplication Events
        self.app.processEvents()
        for name, win in self.windows.items():
            if win.isOpened:
                win.update()

        pass

    def openWindow(self, name) -> bool:
        """
        Show window registered in GUI by it's name.

        :param name: Name of the window in GUI dictionary.
        :return: State of the window (opened = True, closed = False)
        """
        if name in self.windows:
            self.windows[name].open()

        return self.windows[name].isOpened
        pass

    @property
    def isOpened(self) -> bool:
        """
        Checks if any window is opened.

        :return: State of the GUI, if any window is opened - True, else - False
        """
        return any([win.isOpened for win in self.windows.values()])
