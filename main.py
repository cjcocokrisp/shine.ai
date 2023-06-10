from PySide6 import QtWidgets
from gui.gui import MyWidget

import sys

app = QtWidgets.QApplication([])
widget = MyWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())