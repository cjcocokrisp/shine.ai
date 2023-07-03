import pokebase as pb
from PySide6 import QtWidgets
from src.main_menu import MainMenu
from src.settings_tab import SettingsTab
from src.lib.file import File, create_file
from src.lib.cache import cache_names
import os

class StartMenu(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()

        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(NewTab(settings, self), 'New')
        self.tab.addTab(LoadTab(settings, self), 'Load')
        self.tab.addTab(SettingsTab(settings), 'Settings')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tab)

class NewTab(QtWidgets.QWidget):
    def __init__(self, settings, caller):
        super().__init__()

        self.settings = settings
        self.caller = caller

        self.hunt = QtWidgets.QLineEdit('')

        self.mon = QtWidgets.QComboBox()
        self.mon.addItem('')

        if not os.path.isfile('cache/pkmn-names-full.txt'):
            cache_names()

        file = open('cache/pkmn-names-full.txt', 'r')
        full_list = file.readlines()
        for mon in full_list:
            self.mon.addItem(mon.replace('\n', ''))
        file.close()
        self.mon.setEditable(True)

        self.game = QtWidgets.QLineEdit('')
        self.method = QtWidgets.QLineEdit('')
        self.button = QtWidgets.QPushButton('Create')
        self.button.clicked.connect(self.create)

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Hunt Name:'), self.hunt)
        self.layout.addRow(QtWidgets.QLabel('Pokémon:'), self.mon)
        self.layout.addRow(QtWidgets.QLabel('Game:'), self.game)
        self.layout.addRow(QtWidgets.QLabel('Method:'), self.method)
        self.layout.addWidget(self.button)

    def create(self):
        create_file(self.hunt.text(), self.settings.general['default_dir'])
        file = File(f"{self.settings.general['default_dir']}/{self.hunt.text()}.hunt")
        file.update_parameter("Hunt", self.mon.currentText())
        file.update_parameter("Game", self.game.text())
        file.update_parameter("Method", self.method.text())
        os.mkdir(f'data/{self.hunt.text()}')

        self.main_menu = MainMenu(file, self.settings)
        self.main_menu.resize(int(self.settings.general['window_width']) + 200, int(self.settings.general['window_height']) + 200)
        self.main_menu.setWindowTitle('Shine.AI')
        self.main_menu.show()
        self.caller.close()

class LoadTab(QtWidgets.QWidget):
    def __init__(self, settings, caller):
        super().__init__()

        self.settings = settings
        self.caller = caller

        self.explorer = QtWidgets.QFileSystemModel()
        self.explorer.setRootPath('./saves')
        self.explorer.setReadOnly(True)
        self.explorer.setNameFilters(['*.hunt'])
        self.explorer.setNameFilterDisables(False)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.explorer)
        self.tree_view.setRootIndex(self.explorer.index(settings.general['default_dir']))
        self.tree_view.clicked.connect(self.get_explorer_file)

        self.selected_label = QtWidgets.QLabel(f'Selected File: None')

        self.change_dir = QtWidgets.QPushButton('Change Directory')
        self.select = QtWidgets.QPushButton('Select File')
        self.load = QtWidgets.QPushButton('Load')

        self.change_dir.clicked.connect(self.get_new_dir)
        self.select.clicked.connect(self.get_single_file)
        self.load.clicked.connect(self.load_file)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tree_view)
        self.layout.addWidget(self.selected_label)
        self.layout.addWidget(self.change_dir)
        self.layout.addWidget(self.select)
        self.layout.addWidget(self.load)

    def get_explorer_file(self, index):
        file = self.sender().model().filePath(index)
        self.update_selected(file)

    def get_new_dir(self):
        self.dialog = QtWidgets.QFileDialog(self)
        self.dialog.setNameFilter('Folder')
        self.dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if self.dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_dir = self.dialog.selectedFiles()
        self.explorer.setRootPath(new_dir[0])
        self.tree_view.setRootIndex(self.explorer.index(new_dir[0]))

    def get_single_file(self):
        self.dialog = QtWidgets.QFileDialog(self)
        self.dialog.setNameFilter('Hunt Files (*.hunt)')
        self.dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if self.dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            file = self.dialog.selectedFiles()
        self.update_selected(file[0])

    def update_selected(self, file):
        self.selected_label.setText(f'Selected File: {file}')

    def load_file(self):
        selected = self.selected_label.text().replace('Selected File: ', '')
        try:
            file = File(selected)
        except File.InvalidFileError:
            self.dialog = QtWidgets.QErrorMessage()
            self.dialog.setWindowTitle('ERROR')
            self.dialog.showMessage('Not a valid hunt file or the file is corrupted.')
        except FileNotFoundError:
            self.dialog = QtWidgets.QErrorMessage()
            self.dialog.setWindowTitle('ERROR')
            self.dialog.showMessage('File not found or nothing has been selected.')

        self.main_menu = MainMenu(file, self.settings)
        self.main_menu.resize(int(self.settings.general['window_width']) + 200, int(self.settings.general['window_height']) + 200)
        self.main_menu.setWindowTitle('Shine.AI')
        self.main_menu.show()
        self.caller.close()