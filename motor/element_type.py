import sqlite3
import os
from pathlib import Path

class ElementType:

    def __init__(self, code):

        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        self.conn = sqlite3.connect(db_path)

        if type(code) is dict:
            data = code
            code = code['code']
            self.hydrate(data)

        else:
            c = self.conn.cursor()
            c.row_factory = sqlite3.Row
            c.execute("SELECT * FROM `elements_types` WHERE `code` = ? LIMIT 1", (code,))

            data = c.fetchone()

            if not data:
                data = {}

            self.hydrate(data)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        default_values = {
            'name': 'Unnamed',
            'code': 'NV'
        }

        for key in default_values:
            if not key in data:
                data[key] = default_values[key]

        # hydrate data
        self.name = data['name']
        self.code = data['code']

    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `elements_types` WHERE `code` = ? LIMIT 1", (self.code,))
        exists = c.fetchone()

        if not exists:
            c.execute('INSERT INTO `elements_types` VALUES (?,?)', (self.code, self.name))

        else:
            c.execute('UPDATE `elements_types` SET `name` = ? WHERE `code` = ?', (self.name, self.code))

        self.conn.commit()


    # Get all values in a dict
    def getAll(self):
        data = {
            'name': self.name,
            'code': self.code
        }

        return data

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `elements_types` WHERE `code` = ?', (self.code,))
        self.conn.commit()

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        print ("Check elements types table")

        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS `elements_types` (`code` TEXT, `name` TEXT)")

        conn.commit()
        conn.close()