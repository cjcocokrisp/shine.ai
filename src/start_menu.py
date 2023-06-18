from PySide6 import QtCore, QtWidgets, QtGui
from src.lib.file import File, create_file
import sys

class StartMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(NewTab(), 'New')
        self.tab.addTab(LoadTab(), 'Load')
        self.tab.addTab(SettingsTab(), 'Settings')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tab, alignment=QtCore.Qt.AlignTop)

class NewTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hunt = QtWidgets.QLineEdit('')
        self.mon = QtWidgets.QLineEdit('')
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
        create_file(self.hunt.text(), 'saves')
        f = File(f'saves/{self.hunt.text()}.hunt')
        f.update_parameter("Hunt", self.mon.text())
        f.update_parameter("Game", self.game.text())
        f.update_parameter("Method", self.method.text())

class LoadTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.dialog = None

        self.explorer = QtWidgets.QFileSystemModel()
        self.explorer.setRootPath('./saves')
        self.explorer.setReadOnly(True)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.explorer)
        self.tree_view.setRootIndex(self.explorer.index('./saves'))
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
        # TODO: Write all buttons (select file, load, change directory)

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

class SettingsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.win_width = QtWidgets.QLineEdit('')
        self.win_height = QtWidgets.QLineEdit('Test')
        self.button = QtWidgets.QPushButton('Save')

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Theme:'), self.win_width)
        self.layout.addRow(QtWidgets.QLabel('Default Directory:'), self.win_height)
        self.layout.addWidget(self.button)

        # TODO: Figure out settings and write the options and saving button