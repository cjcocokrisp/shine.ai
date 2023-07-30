from PySide6 import QtWidgets, QtGui
from importlib.machinery import SourceFileLoader
from src.lib.gen_cmd_script import gen_cmd_script
from src.lib.screenshot import take_screenshot
import threading

class InputTest(QtWidgets.QScrollArea):

    def __init__(self, file, settings):
        super().__init__()

        self.file = file
        self.settings = settings
        path = gen_cmd_script(file)

        self.label = QtWidgets.QLabel('')
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)

        script = SourceFileLoader('encounter', path).load_module()
        thread = threading.Thread(target=script.encounter, args=(settings, self))
        thread.start()

    def update_text(self, update):
        text = self.label.text() + str(update) + '\n'
        self.label.setText(text)

    def test_screenshot(self):
        path = self.file.path
        while path.find('/') != -1:
            path = path[path.find('/') + 1:]
        path = path[:path.find('.')]
        take_screenshot(f'{path}', self.settings,
                        int(self.settings.hunt['custom_x']), 
                        int(self.settings.hunt['custom_y']),
                        int(self.settings.hunt['custom_width']),
                        int(self.settings.hunt['custom_height']),
                        name='test.png')
        pixmap = QtGui.QPixmap(f'data/{path}/test.png')
        self.label.setPixmap(pixmap)