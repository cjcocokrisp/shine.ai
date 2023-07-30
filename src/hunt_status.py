from PySide6 import QtCore, QtGui, QtWidgets
from src.lib.bot import run_discord_bot
from src.lib.server import run_server
from src.lib.hunt import run_hunt
import threading
from datetime import datetime
import os

class HuntStatus(QtWidgets.QWidget):

    def __init__(self, parent, file, settings):
        super().__init__()

        self.parent = parent
        self.file = file
        self.settings = settings

        self.path = file.path
        while self.path.find('/') != -1:
            self.path = self.path[self.path.find('/') + 1:]
        self.path = self.path[:self.path.find('.')]

        if file.start_time == 'None' and file.start_date == 'None':
            now = datetime.now()
            file.update_parameter('Start Date', str(now.date()))
            file.update_parameter('Start Time', str(now.strftime('%H:%M')))

        self.init_processes()

        self.sprite = QtWidgets.QLabel('')
        pixmap = QtGui.QPixmap(f'./cache/N{file.hunt.lower()}.png')
        self.sprite.setPixmap(pixmap)

        self.encounters = QtWidgets.QLabel(f'Encounters: {file.encounters}')
        self.encounters.setStyleSheet('font-size: 14px;')
        
        self.false_button = QtWidgets.QPushButton('False Find')
        self.false_button.clicked.connect(self.reset)
        self.false_button.setEnabled(False)

        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.close)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.sprite, 0, 0)
        self.layout.addWidget(self.false_button, 1, 0)
        self.layout.addWidget(self.encounters, 0, 1)
        self.layout.addWidget(self.close_button, 1, 1)

    def closeEvent(self, event):
        self.parent.setDisabled(False)
        self.exit_event.set()

    def init_processes(self):
        self.exit_event = threading.Event()
        self.server_thread = threading.Thread(target=run_server, args=(self.exit_event,))
        self.server_thread.daemon = True
        self.hunt_thread = threading.Thread(target=run_hunt, args=(self.file, self.settings, self.exit_event, self))
        self.hunt_thread.daemon = True
        self.bot_thread = threading.Thread(target=run_discord_bot, args=(self.file, self.settings, self.exit_event, self))
        self.bot_thread.daemon = True
        self.server_thread.start()
        self.hunt_thread.start()
        self.bot_thread.start()

    def update_encounters(self, encounters):
        self.encounters.setText(f'Encounters: {str(encounters)}')
        self.file.update_parameter("Encounters", str(encounters))

    def shiny_found(self):
        now = datetime.now()

        self.exit_event.set()
        self.file.set_found(str(now.date()), str(now.strftime('%H:%M')))
        pixmap = QtGui.QPixmap(f'./cache/S{self.file.hunt.lower()}.png')
        self.sprite.setPixmap(pixmap)
        self.encounters.setText(f'Shiny has been found')
        self.false_button.setEnabled(True)

        os.rename(f'data/{self.path}/current.png', f'data/{self.path}/found.png')

    def reset(self):
        self.file.set_found(None, None, reset=True)
        pixmap = QtGui.QPixmap(f'./cache/N{self.file.hunt.lower()}.png')
        self.sprite.setPixmap(pixmap)
        self.encounters.setText('Reset hunt to continue')

        os.remove(f'data/{self.path}/found.png')

    def handle_crash(self):
        self.encounters.setText('Stream has crashed, please reset hunt')
        self.exit_event.set()