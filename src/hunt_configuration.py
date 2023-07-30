from PySide6 import QtCore, QtGui, QtWidgets
from src.lib.screenshot import take_screenshot
from PIL import Image
import os

class ScreenshotConfig(QtWidgets.QWidget):

    def __init__(self, path, settings):
        super().__init__()

        self.path = path
        self.settings = settings

        self.x_edit = QtWidgets.QLineEdit()
        self.x_edit.setValidator(QtGui.QIntValidator(0, 9999999))

        self.width_edit = QtWidgets.QLineEdit()
        self.width_edit.setValidator(QtGui.QIntValidator(0, 9999999))

        self.y_edit = QtWidgets.QLineEdit()
        self.y_edit.setValidator(QtGui.QIntValidator(0, 9999999))

        self.height_edit = QtWidgets.QLineEdit()
        self.height_edit.setValidator(QtGui.QIntValidator(0, 9999999))

        self.test_button = QtWidgets.QPushButton('Test')
        self.test_button.clicked.connect(self.test)

        self.save_button = QtWidgets.QPushButton('Save')
        self.save_button.clicked.connect(self.save)

        if self.settings.hunt['streaming_app'] != 'Custom':
            self.x_edit.setDisabled(True)
            self.y_edit.setDisabled(True)
            self.width_edit.setDisabled(True)
            self.height_edit.setDisabled(True)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(2, 1)
        self.layout.addWidget(QtWidgets.QLabel('X'), 0, 0)
        self.layout.addWidget(self.x_edit, 0, 1)
        self.layout.addWidget(QtWidgets.QLabel('Y'), 1, 0)
        self.layout.addWidget(self.y_edit, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel('Width'), 0, 3)
        self.layout.addWidget(self.width_edit, 0, 4)
        self.layout.addWidget(QtWidgets.QLabel('Height'), 1, 3)
        self.layout.addWidget(self.height_edit, 1, 4)
        self.layout.addWidget(self.test_button, 2, 3)
        self.layout.addWidget(self.save_button, 2, 4)

    def test(self):
        take_screenshot(self.path, 
                        self.settings,
                        self.x_edit.text(),
                        self.y_edit.text(),
                        self.width_edit.text(),
                        self.height_edit.text(),
                        name='test.png')
        self.widget = QtWidgets.QWidget()
        self.widget.layout = QtWidgets.QHBoxLayout(self.widget)
        pixmap = QtWidgets.QLabel('')
        pixmap.setPixmap(QtGui.QPixmap(f'data/{self.path}/test.png'))
        self.widget.layout.addWidget(pixmap)
        self.widget.setWindowTitle('Screenshot Preview')
        self.widget.show()
        os.remove(f'data/{self.path}/test.png')

    def save(self):
        self.settings.change_setting('HUNT', 'custom_x', self.x_edit.text())
        self.settings.change_setting('HUNT', 'custom_y', self.y_edit.text())
        self.settings.change_setting('HUNT', 'custom_width', self.width_edit.text())
        self.settings.change_setting('HUNT', 'custom_height', self.height_edit.text())

class CrashConfig(QtWidgets.QWidget):

    def __init__(self, path):
        super().__init__()

        self.path = path

        self.img = QtWidgets.QLabel('No crash image has been set!')
        if os.path.isfile(f'data/{path}/crash.png'):
            pixmap = QtGui.QPixmap(f'data/{path}/crash.png')
            self.img.setPixmap(pixmap)

        self.set_button = QtWidgets.QPushButton('Set crash image')
        self.set_button.clicked.connect(self.set_img)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.img)
        self.layout.addWidget(self.set_button)

    def set_img(self):
        self.dialog = QtWidgets.QFileDialog(self)
        self.dialog.setNameFilters(['*.png', '*.jpg', '*.jpeg', '*.webp'])
        self.dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if self.dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            file = self.dialog.selectedFiles()

            img = Image.open(file[0])
            img.convert('RGB')
            img.save(f'data/{self.path}/crash.png', 'png')
            img.close()

        pixmap = QtGui.QPixmap(f'data/{self.path}/crash.png')
        self.img.setPixmap(pixmap)