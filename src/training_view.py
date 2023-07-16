from PySide6 import QtWidgets, QtGui, QtCore

class TrainingView(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

    def config_results(self, overall_results, not_results, shiny_results):
        
        self.header = QtWidgets.QLabel('Results')
        self.header.setStyleSheet('font-size: 16px')

        self.setWindowTitle('Model Training Results')

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.close)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.header, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(Results(overall_results, not_results, shiny_results))
        self.layout.addWidget(self.close_button)

class Results(QtWidgets.QWidget):

    class ScoreView(QtWidgets.QWidget):

        def __init__(self, overall_results, not_results, shiny_results):
            super().__init__()

            self.header = QtWidgets.QLabel('Scores:')
            self.header.setStyleSheet('font-size: 14px')

            overall_text = f'Overall Score - {overall_results[0]}% ({overall_results[1]}/{overall_results[2]})'
            not_text = f'Not Shiny Score - {not_results[0]}% ({not_results[1]}/{not_results[2]})'
            shiny_text = f'Shiny Score - {shiny_results[0]}% ({shiny_results[1]}/{shiny_results[2]})'

            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.header, alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(QtWidgets.QLabel(overall_text), alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(QtWidgets.QLabel(not_text), alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(QtWidgets.QLabel(shiny_text), alignment=QtCore.Qt.AlignCenter)

    class ImageView(QtWidgets.QWidget):
        
        class MoveButtons(QtWidgets.QWidget):
            def __init__(self, parent):
                super().__init__()

                self.parent = parent

                self.left_button = QtWidgets.QPushButton('<---')
                self.left_button.clicked.connect(self.left)
                self.right_button = QtWidgets.QPushButton('--->')
                self.right_button.clicked.connect(self.right)

                self.layout = QtWidgets.QHBoxLayout(self)
                self.layout.addWidget(self.left_button)
                self.layout.addWidget(self.right_button)

            def left(self):
                if self.parent.current_index - 1 >= 0:
                    self.parent.update_index(self.parent.current_index - 1)

            def right(self):
                if self.parent.current_index + 1 < len(self.parent.files):
                    self.parent.update_index(self.parent.current_index + 1)

        def __init__(self, not_results, shiny_results):
            super().__init__()

            self.files = []
            self.results = []

            for key in not_results[3]:
                self.files.append(key)
                self.results.append(not_results[3][key])

            for key in shiny_results[3]:
                self.files.append(key)
                self.results.append(shiny_results[3][key])

            self.current_index = 0

            self.header = QtWidgets.QLabel('Test Data Results:')
            self.header.setStyleSheet('font-size: 14px')

            self.img = QtWidgets.QLabel('')
            pixmap = QtGui.QPixmap(self.files[self.current_index])
            pixmap = pixmap.scaled(pixmap.width() / 4, pixmap.height() / 4, QtCore.Qt.KeepAspectRatio)
            self.img.setPixmap(pixmap)

            self.result = QtWidgets.QLabel(self.results[self.current_index])

            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.header, alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.img, alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.result, alignment=QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.MoveButtons(self))

        def update_index(self, index):
            self.current_index = index
            pixmap = QtGui.QPixmap(self.files[self.current_index])
            pixmap = pixmap.scaled(pixmap.width() / 4, pixmap.height() / 4, QtCore.Qt.KeepAspectRatio)
            self.img.setPixmap(pixmap)
            self.result.setText(self.results[self.current_index])

    def __init__(self, overall_results, not_results, shiny_results):
        super().__init__()

        self.score_scroll = QtWidgets.QScrollArea()
        self.score_scroll.setWidget(self.ScoreView(overall_results, not_results, shiny_results))

        self.img_scroll = QtWidgets.QScrollArea()
        self.img_scroll.setWidget(self.ImageView(not_results, shiny_results))

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.score_scroll)
        self.layout.addWidget(self.img_scroll)
        