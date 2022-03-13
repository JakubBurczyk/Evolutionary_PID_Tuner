from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import QtWidgets, uic, QtGui
import sys
from termcolor import colored

from typing import Callable
import scripts.window as window

from abc import ABC


class Widget(ABC):

    def __init__(self, win: window.Window, name: str):
        self._window = win
        self._name = name
        self._widget = getattr(self._window, self._name)
        pass

    @property
    def name(self):
        return self._name

    @property
    def widget(self):
        return self._widget
        pass


class Button(Widget):
    _widget: QPushButton

    def __init__(self, win: window.Window, name: str, function: Callable):
        super(Button, self).__init__(win, name)
        self._widget.clicked.connect(function)
        pass





