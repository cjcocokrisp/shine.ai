from PySide6 import QtCore, QtWidgets, QtGui
import sys

class StartMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(NewTab(), 'New')
        self.tab.addTab(LoadTab(), 'Load')
        self.tab.addTab(SettingsTab(), 'Settings')
        self.tab.currentChanged.connect(self.print_index)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tab, alignment=QtCore.Qt.AlignTop)

    def print_index(self):
        print(f'Index is {self.tab.currentIndex()}')

class NewTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hunt = QtWidgets.QLineEdit('')
        self.mon = QtWidgets.QLineEdit('')
        self.game = QtWidgets.QLineEdit('')
        self.method = QtWidgets.QLineEdit('')
        self.button = QtWidgets.QPushButton('Create')

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Hunt Name:'), self.hunt)
        self.layout.addRow(QtWidgets.QLabel('Pokémon:'), self.mon)
        self.layout.addRow(QtWidgets.QLabel('Game:'), self.game)
        self.layout.addRow(QtWidgets.QLabel('Method:'), self.method)
        self.layout.addWidget(self.button)
        #TODO: CODE BUTTON FUNCTION!!!


class LoadTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.explorer = QtWidgets.QFileSystemModel()
        self.explorer.setRootPath('./saves')
        self.explorer.setReadOnly(True)

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.explorer)
        self.tree_view.setRootIndex(self.explorer.index('./saves'))
        self.tree_view.clicked.connect(self.get_file)

        self.selected = QtWidgets.QLabel('Selected File: None')

        self.change_dir = QtWidgets.QPushButton('Change Directory')
        self.select_file = QtWidgets.QPushButton('Select File')
        self.load = QtWidgets.QPushButton('Load')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tree_view)
        self.layout.addWidget(self.selected)
        self.layout.addWidget(self.change_dir)
        self.layout.addWidget(self.select_file)
        self.layout.addWidget(self.load)
        # TODO: Write button function

    def get_file(self, index):
        path = self.sender().model().filePath(index)
        print(path)

class SettingsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.win_width = QtWidgets.QLineEdit('')
        self.win_height = QtWidgets.QLineEdit('Test')
        self.button = QtWidgets.QPushButton('Save')

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Window Width:'), self.win_width)
        self.layout.addRow(QtWidgets.QLabel('Window Height:'), self.win_height)
        self.layout.addWidget(self.button)