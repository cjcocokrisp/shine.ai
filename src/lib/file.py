class File:
    """
    Procressing for hunt files
    """
    def __init__(self, path:str):
        self.file = open(path, 'r+')
        if self.file.readline() != '<SHINE.AI_HUNT_FILE>\n':
            raise Exception('Not a valid hunt file!')
        
        self.process_log()
        self.process_commands()
        self.process_info()
        
        self.file.seek(0)

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
        
        self.file.seek(0)

    def process_commands(self):
        self.commands = []

        line = self.file.readline()
        while line != '<COMMANDS>\n':
            line = self.file.readline()

        line = self.file.readline()
        while line != '\n':
            self.commands.append(line.replace('\n', ''))
            line = self.file.readline()

        self.file.seek(0)

    def process_info(self):
        line = self.file.readline()
        while line != '<INFO>\n':
            line = self.file.readline()

        self.model_name = self.file.readline().replace('\n','').replace('Model Name: ', '')
        self.passed = bool(self.file.readline().replace('\n','').replace('Passed: ', ''))
        
        self.file.seek(0)

    def close(self):
        self.file.close()