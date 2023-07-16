from PySide6 import QtWidgets, QtGui, QtCore

class TrainingTipsWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.title = QtWidgets.QLabel('Model Training Tips')
        self.title.setStyleSheet('font-size: 16px')

        tips = open('src/lib/training_tips.txt', 'r')
        text = tips.readlines()
        text = ''.join(text)
        tips.close()
        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.close)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(QtWidgets.QLabel(text))
        self.layout.addWidget(self.close_button)