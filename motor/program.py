import json
import os
from pathlib import Path
from datetime import datetime

class Program:

    def __init__(self, skater = 'unamed-skater', program_name = 'program'):

        home_path = str(Path.home())

        if not os.path.exists(home_path + '/.rollartBV/programs/' + skater):
            os.makedirs(home_path + '/.rollartBV/programs/' + skater)

        now = datetime.now()
        nowtime = now.strftime("%Y-%m-%dT%H-%M-%S")
        program_file = home_path + '/.rollartBV/programs/' + skater + '/' +nowtime+ '_' +program_name+'.json'

        try:
            f = open(program_file)
            data = json.load(f)
            self.hydrate(data)
        except IOError:
            self.hydrate({
                'skater': skater,
                'program_name': program_name,
                'start': 0,
                'end': 0,
                'duration': 0,
                'file_time': nowtime,
                'program_elements': []
            })


    # Hydrate values to class
    def hydrate(self, data):
        # check data integrity
        default_values = {
            'skater': 'unamed-skater',
            'program_name': 'program',
            'start': 0,
            'end': 0,
            'duration': 0,
            'file_time': 0,
            'program_elements': []
        }

        for key in default_values:
            if not key in data:
                data[key] = default_values[key]

        # hydrate data
        self.skater = data['skater']
        self.program_name = data['program_name']
        self.start = data['start']
        self.duration = data['duration']
        self.file_time = data['file_time']
        self.program_elements = data['program_elements']

    # record data to json datafile
    def record(self):
        # creating dictionnary
        data = {
            'skater': self.skater,
            'program_name': self.program_name,
            'start': self.start,
            'end': self.end,
            'duration': self.duration,
            'file_time': self.file_time,
            'program_elements': self.program_elements
        }

        # Get path to element file
        home_path = str(Path.home())
        program_file = home_path + '/.rollartBV/programs/' + self.skater + '/' +self.file_time+ '_' +self.program_name+'.json'

        # Replace data or create file
        with open(program_file, 'w') as f:
            json.dump(data, f)

    # Remove element from database
    def delete(self):
        # Get path to element file
        home_path = str(Path.home())
        program_file = home_path + '/.rollartBV/programs/' + self.skater + '/' +self.file_time+ '_' +self.program_name+'.json'

        # Remove file
        os.remove(program_file)

if __name__ == "__main__":
    program = Program()
