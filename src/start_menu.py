from PySide6 import QtWidgets
from src.controls_menu import ControlsMenu
from src.lib.file import File, create_file

class StartMenu(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()

        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(NewTab(), 'New')
        self.tab.addTab(LoadTab(settings), 'Load')
        self.tab.addTab(SettingsTab(settings), 'Settings')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tab)

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
    def __init__(self, settings):
        super().__init__()

        self.dialog = None

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

class SettingsTab(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.theme = QtWidgets.QComboBox()
        self.theme.addItems(['Light', 'Dark'])
        while self.theme.currentText() != self.settings.general['theme']:
            if self.theme.currentIndex() + 1 > self.theme.count():
                self.theme.setCurrentIndex(0)
                self.settings.change_setting('GENERAL', 'theme', self.theme.currentText())
                break
            self.theme.setCurrentIndex(self.theme.currentIndex() + 1)
            
        self.default_dir = ChangeDirButton(settings)

        self.apps = QtWidgets.QComboBox()
        self.apps.addItems(['Snickerstream', 'NTRViewer', 'HzMod TEMP', 'Chokistream',
                            'Elgato TEMP', 'Custom'])
        while self.apps.currentText() != self.settings.hunt['streaming_app']:
            if self.apps.currentIndex() + 1 > self.apps.count() - 1:
                self.apps.setCurrentIndex(0)
                self.settings.change_setting('HUNT', 'streaming_app', self.apps.currentText())
                break
            self.apps.setCurrentIndex(self.apps.currentIndex() + 1)
        self.apps.currentIndexChanged.connect(self.enable_custom_app)

        self.custom_app = QtWidgets.QLineEdit(self.settings.hunt['custom_app'])

        if self.apps.currentText() != 'Custom':
            self.custom_app.setEnabled(False)

        self.use_discord = QtWidgets.QCheckBox()
        if self.settings.hunt['use_discord'] == 'True':
            self.use_discord.setChecked(True)

        self.discord_token = QtWidgets.QLineEdit(self.settings.hunt['discord_token'])

        self.controls = QtWidgets.QPushButton('...')
        self.controls.clicked.connect(self.open_controls_menu)

        self.save_button = QtWidgets.QPushButton('Save')
        self.save_button.clicked.connect(self.save)

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Theme:'), self.theme)
        self.layout.addRow(QtWidgets.QLabel('Default Directory:'), self.default_dir)
        self.layout.addRow(QtWidgets.QLabel('Streaming App:'), self.apps)
        self.layout.addRow(QtWidgets.QLabel('Custom App'), self.custom_app)
        self.layout.addRow(QtWidgets.QLabel('Use Discord:'), self.use_discord)
        self.layout.addRow(QtWidgets.QLabel('Discord Token:'), self.discord_token)
        self.layout.addRow(QtWidgets.QLabel('Set Controls:'), self.controls)
        self.layout.addWidget(self.save_button)

    def enable_custom_app(self):
        if self.apps.currentText() == 'Custom':
            self.custom_app.setEnabled(True)
        else:
            self.custom_app.setEnabled(False)

    def open_controls_menu(self):
        self.control_menu = ControlsMenu(self.settings)
        self.control_menu.resize(int(self.settings.general['window_width']) + 150, int(self.settings.general['window_height']) + 150)
        self.control_menu.setWindowTitle('Set Controls')
        self.control_menu.show()

    def save(self):
        self.settings.change_setting('GENERAL', 'theme', self.theme.currentText())
        self.settings.change_setting('GENERAL', 'default_dir', self.default_dir.current_dir.text())
        self.settings.change_setting('HUNT', 'streaming_app', self.apps.currentText())
        self.settings.change_setting('HUNT', 'custom_app', self.custom_app.text())
        self.settings.change_setting('HUNT', 'use_discord', str(self.use_discord.isChecked()))
        self.settings.change_setting('HUNT', 'discord_token', self.discord_token.text())

class ChangeDirButton(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()

        self.current_dir = QtWidgets.QLabel(settings.general['default_dir'])
        self.button = QtWidgets.QToolButton()
        self.button.setText('...')
        self.button.clicked.connect(self.change_dir)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.current_dir)
        self.layout.addWidget(self.button)

    def change_dir(self):
        self.dialog = QtWidgets.QFileDialog(self)
        self.dialog.setNameFilter('Folder')
        self.dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if self.dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_dir = self.dialog.selectedFiles()
        self.current_dir.setText(new_dir[0])