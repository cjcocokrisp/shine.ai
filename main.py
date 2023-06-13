from PySide6 import QtWidgets, QtGui
from configparser import ConfigParser
from src.start_menu import StartMenu
import ctypes
import sys

myappid = 'cjcocokrisp.shineai'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

settings = ConfigParser()
settings.read('settings.ini')

app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(f'assets/icon.png'))
widget = StartMenu()
widget.resize(settings.getint('WINDOW', 'WINDOW_WIDTH'), settings.getint('WINDOW', 'WINDOW_HEIGHT'))
widget.setWindowTitle('Shine.AI')
widget.show()

sys.exit(app.exec())