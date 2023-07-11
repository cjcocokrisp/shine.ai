from PySide6 import QtWidgets
from importlib.machinery import SourceFileLoader
from src.lib.gen_cmd_script import gen_cmd_script
import threading

class InputTest(QtWidgets.QScrollArea):

    def __init__(self, file, settings):
        super().__init__()

        self.file = file
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