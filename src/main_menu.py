from PySide6 import QtWidgets, QtGui
from src.settings_tab import SettingsTab
from src.lib.cache import cache_img
import pokebase as pb
import urllib.request

class MainMenu(QtWidgets.QWidget):

    def __init__(self, file, settings):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(InfoTab(file), 'Info')
        self.tabs.addTab(StatusTab(), 'Status')
        self.tabs.addTab(HuntTab(), 'Hunt')
        self.tabs.addTab(ConfigureTab(), 'Configure')
        self.tabs.addTab(SettingsTab(settings), 'Settings')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)

class InfoTab(QtWidgets.QWidget):
    def __init__(self, file):
        super().__init__()

        cache_img(file.hunt)
        
class StatusTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class HuntTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class ConfigureTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()