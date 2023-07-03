class File:
    """
    Procressing for hunt files
    """

    class InvalidFileError(Exception):
        def __init__(self, file):
            self.file = file

        def __str__(self):
            return repr('Not a valid hunt file: ' + self.file)

    def read_method(func):
        def wrapper(self):
            func(self)
            self.file.seek(0)
        return wrapper

    def __init__(self, path:str):
        self.path = path
        self.file = open(path, 'r+')
        if self.file.readline() != '<SHINE.AI_HUNT_FILE>\n':
            raise self.InvalidFileError(path)
        
        self.process_log()
        self.process_commands()
        self.process_info()
        self.set_basic_info()

    @read_method
    def process_log(self):
        line = self.file.readline()
        while line != '<LOG>\n':
            line = self.file.readline()

        self.hunt = self.file.readline().replace('\n','').replace('Hunt: ', '')
        self.game = self.file.readline().replace('\n','').replace('Game: ', '')
        self.method = self.file.readline().replace('\n','').replace('Method: ', '')
        self.encounters = int(self.file.readline().replace('\n','').replace('Encounters: ', ''))
        self.phase = int(self.file.readline().replace('\n','').replace('Phase: ', ''))
        self.start_date = self.file.readline().replace('\n','').replace('Start Date: ', '')
        self.start_time = self.file.readline().replace('\n','').replace('Start Time: ', '')
        self.status = self.file.readline().replace('\n', '')
        
    @read_method
    def process_commands(self):
        self.commands = []

        line = self.file.readline()
        while line != '<COMMANDS>\n':
            line = self.file.readline()

        line = self.file.readline()
        while line != '\n':
            self.commands.append(line.replace('\n', ''))
            line = self.file.readline()

    @read_method
    def process_info(self):
        line = self.file.readline()
        while line != '<INFO>\n':
            line = self.file.readline()

        self.model_name = self.file.readline().replace('\n','').replace('Model Name: ', '')
        self.passed = bool(self.file.readline().replace('\n','').replace('Passed: ', ''))
        
    def update_parameter(self, parameter, new_val):

        i = 0 
        line = self.file.readline()
        while line != line.find(parameter) == -1:
            line = self.file.readline()
            i += 1

        self.file.seek(0) 
        lines = self.file.readlines()
        lines[i] = f'{parameter}: {new_val}\n'
        self.file.seek(0)
        self.file.writelines(lines)
        self.file.truncate()
        self.file.seek(0)

        self.process_log()
        self.process_commands()
        self.process_info()
        self.set_basic_info()

    def set_basic_info(self):
        if self.start_time == 'None': 
            temp = 'Not started yet'
        else:  
            temp = f'Started on {self.start_date} at {self.start_time}'
        self.basic_info = {
            'hunt': self.hunt,
            'encounters': self.encounters,
            'game': self.game,
            'method': self.method,
            'start': temp,
            'status': self.status
        }

    def close(self):
        self.file.close()

def create_file(name, directory):
    file = open(f'{directory}/{name}.hunt', 'w')
    template = open('./src/lib/template.txt', 'r')
    lines = template.readlines()
    template.close()
    file.writelines(lines)
    file.close()