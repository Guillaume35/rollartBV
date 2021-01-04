# Rollart unchained
# Copyright (C) 2021  Skaters Team community

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Contributors :
# Guillaume MODARD <guillaumemodard@gmail.com>

import sqlite3
import os
from pathlib import Path
import tools

class Element:

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
            c.row_factory = tools.dict_factory
            c.execute("SELECT * FROM `elements` WHERE `code` = ? LIMIT 1", (code,))

            data = c.fetchone()

            if not data:
                data = {}

            self.hydrate(data)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        default_values = {
            'name': 'Unnamed',
            'code': None,
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
            'qoem3': 0,
            'type': 'NT'
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
        self.type = data['type']

    # record data to database
    def record(self):
        # creating dictionnary
        data = (self.code, self.name, self.base, self.under, self.half, self.down, self.base_combo, self.combo_under, self.combo_half, self.combo_down, self.qoe1, self.qoe2, self.qoe3, self.qoem1, self.qoem2, self.qoem3, self.type)

        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `elements` WHERE `code` = ? LIMIT 1", (self.code,))
        exists = c.fetchone()

        if not exists:
            c.execute('INSERT INTO `elements` VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)

        else:
            c.execute('''UPDATE `elements` SET
                `name` = ?,
                `base` = ?,
                `under` = ?,
                `half` = ?,
                `down` = ?,
                `base_combo` = ?,
                `combo_under` = ?,
                `combo_half` = ?,
                `combo_down` = ?,
                `qoe1` = ?,
                `qoe2` = ?,
                `qoe3` = ?,
                `qoem1` = ?,
                `qoem2` = ?,
                `qoem3` = ?,
                `type` = ?
            WHERE `code` = ?''', (self.name, self.base, self.under, self.half, self.down, self.base_combo, self.combo_under, self.combo_half, self.combo_down, self.qoe1, self.qoe2, self.qoe3, self.qoem1, self.qoem2, self.qoem3, self.type, self.code))

        self.conn.commit()


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
            'qoem3': self.qoem3,
            'type': self.type
        }

        return data

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `elements` WHERE `code` = ?', (self.code,))
        self.conn.commit()

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check elements table")

        c.execute('''CREATE TABLE IF NOT EXISTS `elements`
            (`code` TEXT,
            `name` TEXT,
            `base` REAL,
            `under` REAL,
            `half` REAL,
            `down` REAL,
            `base_combo` REAL,
            `combo_under` REAL,
            `combo_half` REAL,
            `combo_down` REAL,
            `qoe1` REAL,
            `qoe2` REAL,
            `qoe3` REAL,
            `qoem1` REAL,
            `qoem2` REAL,
            `qoem3` REAL,
            `type` TEXT)''')

        c.execute("PRAGMA table_info(`elements`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'code': 'TEXT',
            'name': 'TEXT',
            'base': 'REAL',
            'under': 'REAL',
            'half': 'REAL',
            'down': 'REAL',
            'base_combo': 'REAL',
            'combo_under': 'REAL',
            'combo_half': 'REAL',
            'combo_down': 'REAL',
            'qoe1': 'REAL',
            'qoe2': 'REAL',
            'qoe3': 'REAL',
            'qoem1': 'REAL',
            'qoem2': 'REAL',
            'qoem3': 'REAL',
            'type':'TEXT'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `elements` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()