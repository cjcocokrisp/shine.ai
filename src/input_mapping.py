from PySide6 import QtWidgets, QtGui, QtCore
import PySide6.QtGui
from src.controls_menu import ControlSet, ControlDiagram
from src.timeline_element import TimelineElement
from src.input_test import InputTest 

class InputMappingTool(QtWidgets.QWidget):

    def __init__(self, parent, file, settings):
        super().__init__()

        self.parent = parent

        self.timeline = Timeline(file, settings)
        self.selection = InputSelection(settings, self.timeline)
        self.timeline.connect_selection(self.selection)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(ToolBar(file, settings, self))
        self.layout.addWidget(self.timeline)
        self.layout.addWidget(self.selection)

    def closeEvent(self, event):
        self.parent.setDisabled(False)

class ToolBar(QtWidgets.QWidget):
    
    def __init__(self, file, settings, caller):
        super().__init__()

        self.file = file
        self.settings = settings
        self.caller = caller

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(QtGui.QPixmap('assets/ui/poke-ball.png'))

        self.test_button = QtWidgets.QPushButton('Test')
        self.test_button.clicked.connect(self.test)

        self.save_button = QtWidgets.QPushButton('Save')
        self.save_button.clicked.connect(self.save)

        self.quit_button = QtWidgets.QPushButton('Close')
        self.quit_button.clicked.connect(self.close)

        name = file.path
        while name.find('/') != -1:
            name = name[name.find('/') + 1:]
        name = name[:name.find('.')]

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnStretch(3, 1)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.icon, 0, 0)
        self.layout.addWidget(QtWidgets.QLabel(name), 0, 1, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.test_button, 0, 3, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.save_button, 0, 4, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.quit_button, 0, 5, alignment=QtCore.Qt.AlignRight)

    def test(self):
        self.main_menu = InputTest(self.file, self.settings)
        self.main_menu.resize(int(self.settings.general['window_width']), int(self.settings.general['window_height']))
        self.main_menu.setWindowTitle('Input Test')
        self.main_menu.show()

    def save(self):
        data = self.caller.timeline.diagram_elements
        self.file.write_commands(data)

    def close(self):
        self.caller.close()

class Timeline(QtWidgets.QWidget):

    def __init__(self, file, settings):
        super().__init__()

        self.settings = settings

        self.inputs = QtWidgets.QScrollArea()
        self.inputs.setFixedHeight(400)
        self.load_commands(file)

        self.diagram = ControlDiagram(None, settings, scale_factor=200)
        self.diagram.selection.currentIndexChanged.connect(self.update_selection)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.inputs)
        self.layout.addWidget(self.diagram)

    def connect_selection(self, selection):
        self.selection = selection

    def update_selection(self):
        self.selection.mapper.input_select.clear()
        if self.diagram.selection.currentText() == 'Click to Select':
            console = 'switch'
        else:
            console = self.diagram.selection.currentText().replace(' ', '_').replace('/', '_').lower()
        self.selection.mapper.input_select.addItem('Click to Select')
        for i in range(len(self.selection.mapper.control_set.names)):
            if i in self.diagram.control_indexs[console]:
                item = self.selection.mapper.control_set.names[i].replace('_', ' ').upper()
                self.selection.mapper.input_select.addItem(item)

    def update_diagram(self, modify=False):
        if not modify:
            type_select = self.selection.mapper.type_select.currentText()
            input_button = self.selection.mapper.input_select.currentText()
            cooldown = self.selection.mapper.time_select.text()
            press_interval = self.selection.mapper.interval_select.text()
            self.diagram_elements.append((type_select, input_button, cooldown, press_interval))
        
        self.input_diagram = InputDiagram(self, self.diagram_elements)
        self.inputs.setWidget(self.input_diagram)

    def load_commands(self, file):
        self.diagram_elements = []
        for cmd in file.commands:
            self.diagram_elements.append(cmd.split(','))
        self.update_diagram(modify=True)
            

class InputSelection(QtWidgets.QWidget):

    def __init__(self, settings, timeline):
        super().__init__()

        self.mapper = InputMapper(timeline)

        self.container = QtWidgets.QScrollArea()
        self.container.setFixedSize(int(settings.general['window_width']) + 500, 200)
        self.container.setWidget(self.mapper)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.container)

class InputMapper(QtWidgets.QWidget):

    def __init__(self, timeline):
        super().__init__()

        self.timeline = timeline
        self.control_set = ControlSet(self.timeline.settings)

        self.type_select = QtWidgets.QComboBox()
        self.type_select.addItems(['Click to Select', 'Button Press', 'Repeated Button Press', 'Soft Reset', 'End'])
        self.type_select.currentIndexChanged.connect(self.configure_state)

        self.input_select = QtWidgets.QComboBox()
        self.input_select.addItem('Click to select')
        for control in self.control_set.names:
            self.input_select.addItem(control.replace('_', ' ').upper())
        
        self.time_label = QtWidgets.QLabel('Time Till Next Input (Seconds)')
        self.time_select = QtWidgets.QLineEdit()
        self.time_select.setValidator(QtGui.QIntValidator(0, 9999999))

        self.interval_select = QtWidgets.QLineEdit()
        self.interval_select.setValidator(QtGui.QIntValidator(0, 9999999))

        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.setFixedSize(125, 50)
        self.add_button.clicked.connect(self.add)
        self.remove_button = QtWidgets.QPushButton('Remove')
        self.remove_button.setFixedSize(125, 50)
        self.remove_button.clicked.connect(self.remove)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setHorizontalSpacing(80)
        self.layout.addWidget(QtWidgets.QLabel('Input Type'), 0, 0, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.type_select, 1, 0, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(QtWidgets.QLabel('Button'), 0, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.input_select, 1, 1, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.time_label, 0, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.time_select, 1, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(QtWidgets.QLabel('Press Interval (Seconds)'), 0, 3, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.interval_select, 1, 3, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.add_button, 1, 4, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.remove_button, 3, 4, alignment=QtCore.Qt.AlignRight)

        self.configure_state()

    def configure_state(self):
        typed_selected = self.type_select.currentText()
        if typed_selected == 'Click to Select':
            self.input_select.setEnabled(False)
            self.time_select.setEnabled(False)
            self.add_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.interval_select.setEnabled(False)
        if typed_selected == 'Button Press':
            self.input_select.setEnabled(True)
            self.time_label.setText('Time Till Next Input (Seconds)')
            self.time_select.setEnabled(True)
            self.add_button.setEnabled(True)
            self.interval_select.setEnabled(False)
        if typed_selected == 'Repeated Button Press':
            self.input_select.setEnabled(True)
            self.time_label.setText('Repeat Time (Seconds)')
            self.time_select.setEnabled(True)
            self.add_button.setEnabled(True)
            self.interval_select.setEnabled(True)
        if typed_selected == 'Soft Reset':
            self.input_select.setEnabled(False)
            self.time_label.setText('Game Load Time (Seconds)')
            self.time_select.setEnabled(True)
            self.add_button.setEnabled(True)
            self.interval_select.setEnabled(False)
        if typed_selected == 'End':
            self.input_select.setEnabled(False)
            self.time_label.setText('Time Till Next Input (Seconds)')
            self.time_select.setEnabled(False)
            self.add_button.setEnabled(True)
            self.interval_select.setEnabled(False)

    def add(self):
        if self.add_button.text() == 'Modify': 
            new_data = [
                        self.type_select.currentText(),
                        self.input_select.currentText(),
                        self.time_select.text(),
                        self.interval_select.text()
                       ]
            self.timeline.diagram_elements[self.load_index] = new_data
            modify = True
        else: modify = False
        
        self.timeline.update_diagram(modify=modify)
        self.reset()

    def remove(self):
        self.timeline.diagram_elements.pop(self.load_index)
        self.timeline.update_diagram(modify=True)
        self.reset()

    def load_element(self, index):
        data = self.timeline.diagram_elements[index]
        self.load_index = index
        while self.type_select.currentText() != data[0]:
            self.type_select.setCurrentIndex(self.type_select.currentIndex() + 1)
        self.configure_state()
        while self.input_select.currentText() != data[1]:
            self.input_select.setCurrentIndex(self.input_select.currentIndex() + 1)
        self.time_select.setText(data[2])
        self.interval_select.setText(data[3])
        self.add_button.setText('Modify')
        self.remove_button.setEnabled(True)

    def reset(self):
        self.type_select.setCurrentIndex(0)
        self.input_select.setCurrentIndex(0)
        self.time_select.clear()
        self.interval_select.clear()
        self.add_button.setText('Add')
        self.remove_button.setEnabled(False)
        self.configure_state()


class InputDiagram(QtWidgets.QWidget):

    def __init__(self, caller, element_data):
        super().__init__()

        self.create_elements(caller, element_data)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setVerticalSpacing(150)
        self.layout.addWidget(QtWidgets.QLabel(''), 0, 0)
        for index, element in enumerate(self.elements):
            self.layout.addWidget(element, 1, index)

    def create_elements(self, caller, data):
        self.elements = []
        if len(data) != 0:
            for index, item in enumerate(data):
                element = TimelineElement(caller, index, item[0], item[1], item[2], item[3])
                self.elements.append(element)