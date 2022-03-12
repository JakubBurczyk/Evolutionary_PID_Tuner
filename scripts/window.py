from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import QtWidgets, uic, QtGui
import sys


class Window(QMainWindow):
    def __init__(self, windowName, uiFilePath):
        self._name = windowName
        super(Window, self).__init__()
        uic.loadUi(uiFilePath, self)
        self.openedState = False

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.openedState = False
        print(f"Closing window: {self._name}")
        pass

    def open(self) -> None:
        # print(f"opening window {self._name}")
        if not self.isOpened:
            self.openedState = True
            self.show()
        pass

    def update(self) -> None:
        # print(f"win: {self._name} update")
        pass

    @property
    def isOpened(self) -> bool: return self.openedState

    @property
    def name(self) -> str: return self._name
