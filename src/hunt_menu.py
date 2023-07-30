from PySide6 import QtCore, QtGui, QtWidgets
from src.hunt_configuration import ScreenshotConfig, CrashConfig
from src.hunt_status import HuntStatus

class HuntMenu(QtWidgets.QWidget):
    def __init__(self, parent, file, settings):
        super().__init__()

        path = file.path
        while path.find('/') != -1:
            path = path[path.find('/') + 1:]
        path = path[:path.find('.')]

        self.parent = parent

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(ToolBar(self, path), alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(HuntButtons(self, file, settings, path))
        self.layout.addWidget(QtWidgets.QLabel(f'Streaming App: {settings.hunt["streaming_app"]}'), alignment=QtCore.Qt.AlignBottom)

    def closeEvent(self, event):
        self.parent.setDisabled(False)

class ToolBar(QtWidgets.QWidget):

    def __init__(self, parent, path):
        super().__init__()

        self.parent = parent
        
        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(QtGui.QPixmap('assets/ui/poke-ball.png'))

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.parent.close)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(2, 1)

        self.layout.addWidget(self.icon, 0, 0)
        self.layout.addWidget(QtWidgets.QLabel(path), 0, 1)
        self.layout.addWidget(self.close_button, 0, 3)

class HuntButtons(QtWidgets.QWidget):

    def __init__(self, parent, file, settings, path):
        super().__init__()

        self.parent = parent
        self.file = file
        self.settings = settings
        self.path = path

        self.start_button = QtWidgets.QPushButton('Start Hunt')
        self.start_button.setFixedHeight(int(settings.general['window_height']) / 4)
        self.start_button.clicked.connect(self.begin_hunt)

        self.config_screenshot_button = QtWidgets.QPushButton('Configure Screenshot')
        self.config_screenshot_button.setFixedHeight(int(settings.general['window_height']) / 4)
        self.config_screenshot_button.clicked.connect(self.config_screenshot)
        
        self.config_crash_button = QtWidgets.QPushButton('Configure Crash Detection')
        self.config_crash_button.setFixedHeight(int(settings.general['window_height']) / 4)
        self.config_crash_button.clicked.connect(self.config_crash)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.config_screenshot_button)
        self.layout.addWidget(self.config_crash_button)

    def begin_hunt(self):
        self.dialog = QtWidgets.QMessageBox()
        self.dialog.setText('Please make sure everything to conduct the hunt is open and ready to use!')
        self.dialog.setWindowTitle('WARNING')
        self.dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        self.dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok 
                                        | QtWidgets.QMessageBox.StandardButton.Cancel)
        selection = self.dialog.exec()

        if selection == QtWidgets.QMessageBox.StandardButton.Ok:
            self.hunt_status = HuntStatus(self.parent, self.file, self.settings)
            self.hunt_status.setWindowTitle('Status')
            self.hunt_status.show()
            self.parent.setDisabled(True)

    def config_screenshot(self):
        self.screenshot_config = ScreenshotConfig(self.path, self.settings)
        self.screenshot_config.setWindowTitle('Screenshot Configuration Tool')
        self.screenshot_config.show()

    def config_crash(self):
        self.crash_config = CrashConfig(self.path)
        self.crash_config.setWindowTitle('Crash Configuration Tool')
        self.crash_config.show()