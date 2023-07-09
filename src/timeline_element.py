from PySide6 import QtWidgets, QtGui, QtCore

class TimelineElement(QtWidgets.QWidget):

    def __init__(self, timeline, index, input_type, input_button, time, press_interval):
        super().__init__()

        self.timeline = timeline
        self.index = index

        self.input_type = input_type
        self.input_button = input_button
        self.time = time
        self.press_interval = press_interval

        if input_type == 'Button Press':
            text = f'Input {input_button}'
        elif input_type == 'Repeated Button Press':
            text = f'Repeated Input {input_button} every {press_interval} seconds'
        elif input_type == 'Soft Reset':
            text = 'Soft Reset'
        elif input_type == 'End':
            text = 'End'

        self.input_label = QtWidgets.QLabel(text)
        self.input_label.setStyleSheet('font-size: 20px;')

        if text != 'End':
            self.time_label = QtWidgets.QLabel(f'----{time}--->')
        else:
            self.time_label = QtWidgets.QLabel('')
        self.time_label.setStyleSheet('font-size: 14px;')

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.time_label)

    def mouseDoubleClickEvent(self, event):
        self.timeline.selection.mapper.load_element(self.index)