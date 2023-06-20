from configparser import ConfigParser
from dataclasses import dataclass
from os.path import isfile

@dataclass
class Settings():
    general = {
                'window_width':500,
                'window_height':400,
                'theme':'Light',
                'default_dir':'./saves'
              }
    hunt = {
             'streaming_app':'snickerstream',
             'use_discord': True,
             'discord_token': None
           }
    control = {
                'left': None,
                'right': None,
                'up': None,
                'down': None,
                'a': None,
                'b': None,
                'x': None,
                'y': None,
                'l': None,
                'r': None,
                'zl': None,
                'zr': None,
                'start': None,
                'select': None,
                'home': None
              }

    def load_settings(self):
        if isfile('settings.ini'):
            self.parser = ConfigParser()
            self.parser.read('settings.ini')

            for item in self.parser.items('GENERAL'):
                self.general[item[0]] = item[1]

            for item in self.parser.items('HUNT'):
                self.hunt[item[0]] = item[1]

            for item in self.parser.items('GENERAL'):
                self.control[item[0]] = item[1]

        else:
            self.create_file()

    def create_file(self):
        fp = open('settings.ini', 'w')
        fp.write('[GENERAL]\n')
        
        for key in self.general.keys():
            fp.write(f'{key} = {self.general[key]}\n')
        fp.write('\n')

        for key in self.hunt.keys():
            fp.write(f'{key} = {self.hunt[key]}\n')
        fp.write('\n')

        for key in self.control.keys():
            fp.write(f'{key} = {self.control[key]}\n')

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