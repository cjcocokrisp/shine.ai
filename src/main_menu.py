from PySide6 import QtWidgets, QtGui
from src.settings_tab import SettingsTab
import pokebase as pb
import urllib.request

class MainMenu(QtWidgets.QWidget):

    def __init__(self, file, settings):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(InfoTab(), 'Info')
        self.tabs.addTab(StatusTab(), 'Status')
        self.tabs.addTab(HuntTab(), 'Hunt')
        self.tabs.addTab(ConfigureTab(), 'Configure')
        self.tabs.addTab(SettingsTab(settings), 'Settings')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)

class InfoTab(QtWidgets.QWidget):
    def __init__(self):
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


        # self.file = file

        # self.mon_api_data = pb.APIResource('pokemon', self.file.hunt.lower())

        # try:
        #     if file.status.find('not') == -1:
        #         sprite = pb.SpriteResource('pokemon', str(self.mon_api_data.id), shiny=True)
        #         img_type = 'shiny'
        #     else:
        #         sprite = pb.SpriteResource('pokemon', str(self.mon_api_data.id))
        #         img_type = 'normal'

        #         urllib.request.urlretrieve(str(sprite.url), 
        #                                 f'assets/mons/{img_type}/{str(self.mon_api_data.id)}.png')
        #         img_path = f'assets/mons/{img_type}/{str(self.mon_api_data.id)}.png'
        # except AttributeError:
        #     img_path = f'assets/ui/unknown.png'            


        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.test = QtWidgets.QLabel()
        # self.test.setPixmap(QtGui.QPixmap(img_path))
        # self.layout.addWidget(self.test)