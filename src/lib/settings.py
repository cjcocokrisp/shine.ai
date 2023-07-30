from configparser import ConfigParser
from dataclasses import dataclass
from os.path import isfile

@dataclass
class Settings():
    general = {
                'window_width':500,
                'window_height':400,
                'theme':'Light',
                'default_dir':'./saves',
                'low_storage': 'False'
              }
    hunt = {
             'streaming_app':'Snickerstream',
             'custom_app':'',
             'custom_x':0,
             'custom_y':0,
             'custom_width':0,
             'custom_height':0,
             'use_discord': 'True',
             'discord_token': 'Not Set',
             'spam_channel': 'Not Set'
           }
    control = {
                'laxis_hor': '',
                'laxis_ver': '',
                'raxis_hor': '',
                'raxis_ver': '',
                'dpad_left': '',
                'dpad_right': '',
                'dpad_up': '',
                'dpad_down': '',
                'a': '',
                'b': '',
                'x': '',
                'y': '',
                'l': '',
                'r': '',
                'zl': '',
                'zr': '',
                'start': '',
                'select': '',
                'home': ''
              }
    
    def load_settings(self):
        if isfile('settings.ini'):
            self.parser = ConfigParser()
            self.parser.read('settings.ini')

            for item in self.parser.items('GENERAL'):
                self.general[item[0]] = item[1]

            for item in self.parser.items('HUNT'):
                self.hunt[item[0]] = item[1]

            for item in self.parser.items('CONTROL'):
                self.control[item[0]] = item[1]

        else:
            self.create_file()

    def create_file(self):
        fp = open('settings.ini', 'w')
        
        fp.write('[GENERAL]\n')
        for key in self.general.keys():
            fp.write(f'{key} = {self.general[key]}\n')
        fp.write('\n')

        fp.write('[HUNT]\n')
        for key in self.hunt.keys():
            fp.write(f'{key} = {self.hunt[key]}\n')
        fp.write('\n')

        fp.write('[CONTROL]\n')
        for key in self.control.keys():
            fp.write(f'{key} = {self.control[key]}\n')

        self.parser = ConfigParser()
        self.parser.read('settings.ini')

    def change_setting(self, section, name, value):
        self.parser.set(section, name, value)

        fp = open('settings.ini', 'w')
        self.parser.write(fp)

        if section == 'GENERAL':
            self.general[name] = value
        elif section == 'HUNT':
            self.hunt[name] = value
        elif section == 'CONTROL':
            self.control[name] = value