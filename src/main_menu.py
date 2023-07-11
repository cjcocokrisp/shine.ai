from PySide6 import QtWidgets, QtGui, QtCore
from discord.ext import commands
from src.settings_tab import SettingsTab
from src.lib.cache import cache_mon_img
import src.start_menu
import src.input_mapping
from os.path import isfile
from discord import Intents

class MainMenu(QtWidgets.QWidget):

    def __init__(self, file, settings):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(InfoTab(file, settings), 'Info')
        self.tabs.addTab(StatusTab(file, settings), 'Status')
        self.tabs.addTab(HuntTab(), 'Hunt')
        self.tabs.addTab(ConfigureTab(self, file, settings), 'Configure')
        self.tabs.addTab(SettingsTab(self, settings), 'Settings')

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
    def __init__(self, file, settings):
        super().__init__()

        self.settings = settings
        if self.settings.hunt['use_discord'] == 'True':
            self.test_discord_connection()
            if self.bot_passed:
                self.bot_status = 'Valid Discord Bot Token'
            else:
                self.bot_status = 'Invalid Discord Bot Token'
        else:
            self.bot_status = 'Discord Updates Are Not Being Used'
            
        self.bot_label = QtWidgets.QLabel(self.bot_status)
        self.bot_label.setStyleSheet('font-size: 14pt;')

        self.model_label = QtWidgets.QLabel(f'Model Accuracy: {file.accuracy}')
        self.model_label.setStyleSheet('font-size: 14pt;')

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.bot_label, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.model_label, alignment=QtCore.Qt.AlignCenter)

    def test_discord_connection(self):
        client = commands.Bot(command_prefix='TEST', intents=Intents.default())
        
        @client.event
        async def on_ready():
            self.bot_passed = True
            await client.close()

        try:
            client.run(self.settings.hunt['discord_token'])
        except:
            self.bot_passed = False

class HuntTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class ConfigureTab(QtWidgets.QWidget):
    def __init__(self, parent, file, settings):
        super().__init__()

        self.parent = parent
        self.file = file
        self.settings = settings

        self.inputs = QtWidgets.QPushButton('Input Mapping Tool')
        self.training = QtWidgets.QPushButton('Model Training Suite')
        self.inputs.setFixedHeight(int(settings.general['window_height']) / 4)
        self.training.setFixedHeight(int(settings.general['window_height']) / 4)

        self.inputs.clicked.connect(self.load_control_mapping)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.inputs)
        self.layout.addWidget(self.training)

    def load_control_mapping(self):
        self.control_mapping = src.input_mapping.InputMappingTool(self.parent, self.file, self.settings)
        self.control_mapping.resize(int(self.settings.general['window_width']) + 500, int(self.settings.general['window_height']) + 250)
        self.control_mapping.setWindowTitle('Input Mapping Tool')
        self.control_mapping.show()
        self.parent.setDisabled(True)

    def load_model_training(self):
        pass

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

        info = ''
        for key in self.file.basic_info.keys():
            info += f'{key.capitalize()}: {self.file.basic_info[key]}'
            info += '\n'

        self.info = QtWidgets.QLabel(info)
        self.info.setStyleSheet('font-size: 14pt;')

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sprite)
        self.layout.addWidget(self.info)