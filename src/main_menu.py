from PySide6 import QtWidgets, QtGui, QtCore
from src.settings_tab import SettingsTab
from src.lib.cache import cache_img, cache_mon_img
import src.start_menu
from os.path import isfile

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
        self.layout.addWidget(DisplayBar(file, settings, self))
        self.layout.addWidget(self.tabs)

class InfoTab(QtWidgets.QWidget):
    def __init__(self, file):
        super().__init__()

        
class StatusTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class HuntTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class ConfigureTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class DisplayBar(QtWidgets.QWidget):
    def __init__(self, file, settings, caller):
        super().__init__()

        self.file = file
        self.settings = settings
        self.caller = caller

        if not isfile('cache/poke-ball.png'):
            cache_img('items/gen5', 'poke-ball')

        self.mon = QtWidgets.QLabel()
        self.mon.setPixmap(QtGui.QPixmap(f'cache/poke-ball.png'))

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.close)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnStretch(3, 1)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.mon)

        name = file.path
        while name.find('/') != -1:
            name = name[name.find('/') + 1:]
            print(name)
        name = name[:name.find('.')]

        self.layout.addWidget(QtWidgets.QLabel(name), 0, 1, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.close_button, 0, 3, alignment=QtCore.Qt.AlignRight)
        
    def close(self):
        self.file.close()

        self.main_menu = src.start_menu.StartMenu(self.settings)
        self.main_menu.resize(int(self.settings.general['window_width']), int(self.settings.general['window_height']))
        self.main_menu.setWindowTitle('Shine.AI')
        self.main_menu.show()
        self.caller.close()