from PySide6 import QtWidgets, QtGui
from src.lib.settings import Settings
from src.lib.cache import clear_cache
from src.start_menu import StartMenu
import ctypes
import os
import qdarktheme

myappid = 'cjcocokrisp.shineai'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

settings = Settings()
settings.load_settings()

if not os.path.isdir('cache'):
    os.mkdir('cache')
    
if not os.path.isdir('saves'):
    os.mkdir('saves')

if not os.path.isdir('data'):
    os.mkdir('data')

app = QtWidgets.QApplication([])
if settings.general['theme'] == 'Dark':
    qdarktheme.setup_theme()
else:
    qdarktheme.setup_theme('light')
app.setWindowIcon(QtGui.QIcon(f'assets/ui/icon.png'))
widget = StartMenu(settings)
widget.resize(int(settings.general['window_width']), int(settings.general['window_height']))
widget.setWindowTitle('Shine.AI')
widget.show()

app.exec()

if settings.general['low_storage'] == 'True':
    clear_cache()