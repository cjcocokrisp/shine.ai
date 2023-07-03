from PySide6 import QtWidgets, QtGui, QtCore
from src.settings_tab import SettingsTab
from src.lib.cache import cache_mon_img
import src.start_menu
from os.path import isfile

class MainMenu(QtWidgets.QWidget):

    def __init__(self, file, settings):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(InfoTab(file, settings), 'Info')
        self.tabs.addTab(StatusTab(), 'Status')
        self.tabs.addTab(HuntTab(), 'Hunt')
        self.tabs.addTab(ConfigureTab(), 'Configure')
        self.tabs.addTab(SettingsTab(settings), 'Settings')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(DisplayBar(file, settings, self))
        self.layout.addWidget(self.tabs)

class InfoTab(QtWidgets.QWidget):
    def __init__(self, file, settings):
        super().__init__()

        self.w = int(settings.general['window_width'])
        self.h = int(settings.general['window_height'])
        self.file = file

        self.info = InfoDisplay(file, self.w, self.h)

        self.screenshot = QtWidgets.QLabel()
        if self.file.status.find('not') == -1:
            name = self.file.path
            while name.find('/') != -1:
                name = name[name.find('/') + 1:]
            name = name[:name.find('.')]
            ss_path = f'data/{name}/found.png'
        else:
            ss_path = 'assets/ui/ssplaceholder.png'
        self.screenshot.setPixmap(QtGui.QPixmap(ss_path))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.screenshot, alignment=QtCore.Qt.AlignCenter)
        
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

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(QtGui.QPixmap(f'assets/ui/poke-ball.png'))

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.close)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnStretch(3, 1)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.icon)

        name = file.path
        while name.find('/') != -1:
            name = name[name.find('/') + 1:]
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

class InfoDisplay(QtWidgets.QWidget):

    def __init__(self, file, width, height):
        super().__init__()

        self.file = file
        self.w = width
        self.h = height

        if not isfile(f'cache/N{file.hunt.lower()}.png') or not isfile(f'cache/S{file.hunt.lower()}.png'):
            status = cache_mon_img(file.hunt.lower())
        else: status = True

        self.sprite = QtWidgets.QLabel()
        if status:
            if file.status.find('not') == -1: tag = 'S'
            else: tag = 'N'
            sprite_path = f'cache/{tag}{file.hunt.lower()}.png'
        else: sprite_path = f'assets/ui/unknown.png'

        pixmap = QtGui.QPixmap(sprite_path)
        pixmap = pixmap.scaled(self.w - 180, self.h - 180, QtCore.Qt.KeepAspectRatio)
        self.sprite.setPixmap(pixmap)

        info = 'Shiny Hunt Information:'
        for key in self.file.basic_info.keys():
            info += '\n'
            info += f'{key.capitalize()}: {self.file.basic_info[key]}'

        self.info = QtWidgets.QLabel(info)
        self.info.setStyleSheet('font-size: 14pt;')

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sprite)
        self.layout.addWidget(self.info)