from PyQt5.QtWidgets import *
from typing import List, Dict
from window import *
import os


class GUI:
    def __init__(self):
        self.uisDir = os.path.abspath(os.path.join(os.path.realpath(__file__), "../"*2, "uis"))
        self.windows: Dict[str, Window] = {}
        self.app = QtWidgets.QApplication([])
        print(colored("Initializing GUI",'green'))
        pass

    def addWindow(self, name: str, file: str):
        if name not in self.windows.keys():
            self.windows[name] = Window(name, os.path.join(self.uisDir, file))
        else:
            raise AttributeError("That window already exists")
        pass

    def start(self):
        #print("Starting GUI")
        while any([win.isOpened for win in self.windows.values()]):
            self.update()
        pass

    def update(self):
        # processing QtApplication Events
        self.app.processEvents()
        for name, win in self.windows.items():
            if win.isOpened:
                win.update()

        pass

    def openWindow(self, name):
        if name in self.windows:
            self.windows[name].open()
        pass