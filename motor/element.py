import json
import os
from pathlib import Path

class Element:

    def __init__(self, code):

        home_path = str(Path.home())

        if not os.path.exists(home_path + '/.rollartBV/elements'):
            os.makedirs(home_path + '/.rollartBV/elements')

        if type(code) is dict:
            data = code
            code = code['code']
            self.hydrate(data)

        else:
            table_file = home_path + '/.rollartBV/elements/' + code + '.json'

            with open(table_file) as f:
                data = json.load(f)
                self.hydrate(data)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        default_values = {
            'name': 'Unnamed',
            'code': 'NV',
            'base': 0,
            'under': 0,
            'half': 0,
            'down': 0,
            'base_combo': 0,
            'combo_under': 0,
            'combo_half': 0,
            'combo_down': 0,
            'qoe1': 0,
            'qoe2': 0,
            'qoe3': 0,
            'qoem1': 0,
            'qoem2': 0,
            'qoem3': 0
        }

        for key in default_values:
            if not key in data:
                data[key] = default_values[key]

        # hydrate data
        self.name = data['name']
        self.code = data['code']
        self.base = data['base']
        self.under = data['under']
        self.half = data['half']
        self.down = data['down']
        self.base_combo = data['base_combo']
        self.combo_under = data['combo_under']
        self.combo_half = data['combo_half']
        self.combo_down = data['combo_down']
        self.qoe1 = data['qoe1']
        self.qoe2 = data['qoe2']
        self.qoe3 = data['qoe3']
        self.qoem1 = data['qoem1']
        self.qoem2 = data['qoem2']
        self.qoem3 = data['qoem3']

    # record data to json datafile
    def record(self):
        # creating dictionnary
        data = {
            'name': self.name,
            'code': self.code,
            'base': self.base,
            'under': self.under,
            'half': self.half,
            'down': self.down,
            'base_combo': self.base_combo,
            'combo_under': self.combo_under,
            'combo_half': self.combo_half,
            'combo_down': self.combo_down,
            'qoe1': self.qoe1,
            'qoe2': self.qoe2,
            'qoe3': self.qoe3,
            'qoem1': self.qoem1,
            'qoem2': self.qoem2,
            'qoem3': self.qoem3
        }

        # Get path to element file
        home_path = str(Path.home())
        table_file = home_path + '/.rollartBV/elements/' + self.code + '.json'

        # Replace data or create file
        with open(table_file, 'w') as f:
            json.dump(data, f)


    # Get all values in a dict
    def getAll(self):
        data = {
            'name': self.name,
            'code': self.code,
            'base': self.base,
            'under': self.under,
            'half': self.half,
            'down': self.down,
            'base_combo': self.base_combo,
            'combo_under': self.combo_under,
            'combo_half': self.combo_half,
            'combo_down': self.combo_down,
            'qoe1': self.qoe1,
            'qoe2': self.qoe2,
            'qoe3': self.qoe3,
            'qoem1': self.qoem1,
            'qoem2': self.qoem2,
            'qoem3': self.qoem3
        }

        return data

    # Remove element from database
    def delete(self):
        # Get path to element file
        home_path = str(Path.home())
        table_file = home_path + '/.rollartBV/elements/' + self.code + '.json'

        # Remove file
        os.remove(table_file)

if __name__ == "__main__":
    element = Element()
