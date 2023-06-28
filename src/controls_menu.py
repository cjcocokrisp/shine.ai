from PySide6 import QtWidgets, QtGui, QtCore

class ControlsMenu(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(ControlSet(settings))
        self.layout.addWidget(ControlDiagram(self.layout.itemAt(0).widget(), settings))

class ControlSet(QtWidgets.QWidget):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.edits = []
        self.labels = []
        self.names = [x for x in self.settings.control.keys()]
        
        self.layout = QtWidgets.QFormLayout(self)
        for i in range(len(self.names)):
            self.labels.append(QtWidgets.QLabel(self.names[i].replace('_', ' ').upper()))
            self.edits.append(QtWidgets.QLineEdit(self.settings.control[self.names[i]]))
            self.edits[i].setMaximumWidth(int(self.settings.general['window_width']) / 20)
            self.layout.addRow(self.labels[i], self.edits[i])

        self.save = QtWidgets.QPushButton('Save')
        self.save.setMaximumWidth(int(self.settings.general['window_width']) / 10)
        self.save.clicked.connect(self.save_controls)
        self.layout.addWidget(self.save)


    def save_controls(self):
        for i in range(len(self.names)):
            self.settings.change_setting('CONTROL', self.names[i], self.edits[i].text())

class ControlDiagram(QtWidgets.QWidget):

    control_indexs = {
        'gameboy': [4, 5, 6, 7, 8, 9, 16, 17],
        'gameboy_advance': [4, 5, 6, 7, 8, 9, 12, 13, 16, 17],
        'ds_3ds': [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18],
        'switch': [x for x in range(19)],

    }

    def __init__(self, control_set, settings):
        super().__init__()

        self.control_set = control_set
        self.settings = settings

        self.w = int(self.settings.general['window_width'])
        self.h = int(self.settings.general['window_height'])

        self.selection = QtWidgets.QComboBox()
        self.selection.addItems(['Click to Select', 'Gameboy', 'Gameboy Advance', 'DS/3DS', 'Switch'])
        self.selection.currentIndexChanged.connect(self.change_view)
        self.selection.setFixedSize(self.w / 4, self.h / 20)

        self.image = QtWidgets.QLabel('Select a console to view controls for it.')
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.selection, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.image)

    def change_view(self):
        console = self.selection.currentText().replace(' ', '_').replace('/', '_').lower()
        if console in self.control_indexs.keys():
            self.image.setPixmap(QtGui.QPixmap(f'assets/console/{console}.png').scaled(self.w - 60, self.h - 60, QtCore.Qt.KeepAspectRatio))
            for i in range(len(self.control_set.names)):
                if i in self.control_indexs[console]:
                    self.control_set.labels[i].setStyleSheet('background-color: rgb(74, 224, 92)')
                else:
                    self.control_set.labels[i].setStyleSheet('background-color: rgb(224, 74, 74)')
        else:
            self.image.setText('Select a console to view controls for it.')
            for i in range(len(self.control_set.names)):
                self.control_set.labels[i].setStyleSheet('')


