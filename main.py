from PySide6 import QtWidgets, QtGui
from src.lib.settings import Settings
from src.start_menu import StartMenu
import ctypes
import sys

myappid = 'cjcocokrisp.shineai'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

settings = Settings()
settings.load_settings()

app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(f'assets/icon.png'))
widget = StartMenu()
widget.resize(int(settings.general['window_width']), int(settings.general['window_height']))
widget.setWindowTitle('Shine.AI')
widget.show()

sys.exit(app.exec())