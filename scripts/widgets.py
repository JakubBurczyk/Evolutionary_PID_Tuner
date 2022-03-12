from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from termcolor import colored

from typing import Callable


class Widget:
    def __init__(self, win, name: str):
        self._window = win
        self._name = name
        self.widget = getattr(self._window, self._name)
        pass

    @property
    def name(self):
        return self._name


class Button(Widget):
    widget: QPushButton

    def __init__(self, win, name: str, function: Callable, *args, **kwargs):
        super(Button, self).__init__(win, name)
        print(args)
        print(kwargs)
        self.widget.clicked.connect(function)
        pass


