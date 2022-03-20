import datetime

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


class LCD(Widget):
    _widget: QLCDNumber
    getValue: Callable

    def __init__(self, win: window.Window, name: str):
        super(LCD, self).__init__(win, name)

        self._value = 0
        self.frequency = 5 #Hz
        self.updateDt = 1/self.frequency
        self.lastUpdate = datetime.datetime.now()
        self.getValue = None
        pass

    def setCallback(self, function: Callable):
        self.getValue = function
        pass

    def setValue(self, value):
        #print(f"LCD: {self.name} displaying: {self.value}")
        self._value = value
        pass

    def display(self, value):
        #print(f"LCD: {self.name} displaying: {self.value}")
        self._widget.display(value)
        pass

    def update(self):
        print(self._value)

    def update(self):

        dt_ms = (datetime.datetime.now() - self.lastUpdate).total_seconds()
        if dt_ms >= self.updateDt:
            if self.getValue is not None:
                self._value = self.getValue()
                self.lastUpdate = datetime.datetime.now()

            self.display(self.value)
        else:
            pass

    @property
    def updateable(self):
        return self.getValue is not None
        pass

    @property
    def value(self):
        return self._value
        pass




