import datetime

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from termcolor import colored
from typing import Dict, Callable
import scripts.widgets as widgets


class Window(QMainWindow):

    def __init__(self, windowName, uiFilePath):
        """
        Class describing a window that can be show on the screen.

        :param windowName: name of the window in dictionary
        :param uiFilePath: Path to the .ui files directory
        """
        self._name = windowName
        super(Window, self).__init__()
        uic.loadUi(uiFilePath, self)
        self.openedState = False

        self.buttons: Dict[str, widgets.Button] = {}
        self.lcds: Dict[str, widgets.LCD] = {}
        self.spinboxes: Dict[str, widgets.SpinBoxAbstract] = {}

    def say(self, msg=None):
        print(self._name + " | MSG = " + msg)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """
        Handle window closing event.

        :param a0: Close event sent (Qt internals)
        :return: None
        """
        self.openedState = False
        print(colored(f"Closing window: {self._name}", 'red'))
        pass

    def open(self) -> None:
        """
        Show the window on the screen.

        :return: None
        """
        # print(f"opening window {self._name}")
        if not self.openedState:
            self.openedState = True
            self.show()
        pass

    def update(self) -> None:
        """
        Update window and widgets on it.

        :return: None
        """
        #print(f"\rwin: {self._name} update {datetime.datetime.now()}",end = "")
        for name, lcd in self.lcds.items():
            if lcd.updateable:
                lcd.update()
        pass

    def addButton(self, name, function: Callable):
        self.buttons[name] = widgets.Button(self, name, function)

    def addLCD(self, name):
        self.lcds[name] = widgets.LCD(self, name)

    def addSpinBox(self, name, double=False):
        spinbox = None
        if double is False:
            spinbox = widgets.SpinBox(self, name)
        else:
            spinbox = widgets.DoubleSpinBox(self, name)

        self.spinboxes[name] = spinbox

    @property
    def isOpened(self) -> bool:
        """
        Check whether the window is currently opened.

        :return: True if window is opened otherwise False
        """
        return self.openedState

    @property
    def name(self) -> str:
        """
        Get property name of the window.

        :return: str
        """
        return self._name
