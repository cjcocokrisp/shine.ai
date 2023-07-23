from PySide6 import QtWidgets
from src.controls_menu import ControlsMenu
from src.lib.cache import clear_cache
import qdarktheme

class SettingsTab(QtWidgets.QWidget):
    def __init__(self, parent, settings):
        super().__init__()

        self.settings = settings
        self.parent = parent

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
        
        self.low_storage = QtWidgets.QCheckBox()
        if self.settings.general['low_storage'] == 'True':
            self.low_storage.setChecked(True)

        self.controls = QtWidgets.QPushButton('...')
        self.controls.clicked.connect(self.open_controls_menu)

        self.save_button = QtWidgets.QPushButton('Save')
        self.save_button.clicked.connect(self.save)

        self.cache_button = QtWidgets.QPushButton('Clear Cache')
        self.cache_button.clicked.connect(clear_cache)

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Theme:'), self.theme)
        self.layout.addRow(QtWidgets.QLabel('Default Directory:'), self.default_dir)
        self.layout.addRow(QtWidgets.QLabel('Streaming App:'), self.apps)
        self.layout.addRow(QtWidgets.QLabel('Custom App'), self.custom_app)
        self.layout.addRow(QtWidgets.QLabel('Use Discord:'), self.use_discord)
        self.layout.addRow(QtWidgets.QLabel('Discord Token:'), self.discord_token)
        self.layout.addRow(QtWidgets.QLabel('Low Storage Mode:'), self.low_storage)
        self.layout.addRow(QtWidgets.QLabel('Set Controls:'), self.controls)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cache_button)

    def enable_custom_app(self):
        if self.apps.currentText() == 'Custom':
            self.custom_app.setEnabled(True)
        else:
            self.custom_app.setEnabled(False)

    def open_controls_menu(self):
        self.control_menu = ControlsMenu(self.parent, self.settings)
        self.control_menu.resize(int(self.settings.general['window_width']) + 150, int(self.settings.general['window_height']) + 150)
        self.control_menu.setWindowTitle('Set Controls')
        self.control_menu.show()
        self.parent.setDisabled(True)

    def save(self):

        if self.settings.general['theme'] != self.theme.currentText():
            qdarktheme.setup_theme(self.theme.currentText().lower())

        self.settings.change_setting('GENERAL', 'theme', self.theme.currentText())
        self.settings.change_setting('GENERAL', 'default_dir', self.default_dir.current_dir.text())
        self.settings.change_setting('HUNT', 'streaming_app', self.apps.currentText())
        self.settings.change_setting('HUNT', 'custom_app', self.custom_app.text())
        self.settings.change_setting('HUNT', 'use_discord', str(self.use_discord.isChecked()))
        self.settings.change_setting('HUNT', 'discord_token', self.discord_token.text())
        self.settings.change_setting('GENERAL', 'low_storage', str(self.low_storage.isChecked()))

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