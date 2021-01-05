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
from motor.element import *

class ProgramElement:

    def __init__(self, data=0):

        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        self.conn = sqlite3.connect(db_path)

        data_id = data

        if type(data) is dict:
            if 'id' in data:
                data_id = data['id']
            
            else:
                data_id  = 0
            
            self.hydrate(data)

        else:
            c = self.conn.cursor()
            c.row_factory = tools.dict_factory
            c.execute("SELECT * FROM `program_elements` WHERE `id` = ? LIMIT 1", (data_id,))

            values = c.fetchone()

            if not values:
                values = {}

            self.hydrate(values)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'program': 0,
            'box': 0,
            'type': "SoloJump",
            'label': "2 Toeloop",
            'code': "2T",
            'value_label': 'base',
            'base_value': 1.7,
            'bonus': '',
            'bonus_value': 0.0,
            'qoe': 0,
            'qoe_value': 0,
            'technical_value': 1.7,
            'star': 0,
            'stared_value': 1.7,
            'time': 0
        }

        for key in values:
            if key in data:
                values[key] = data[key]

        # hydrate data
        self.id = values['id']
        self.program = values['program']
        self.box = values['box']
        self.type = values['type']
        self.label = values['label']
        self.code = values['code']
        self.value_label = values['value_label']
        self.base_value = values['base_value']
        self.bonus = values['bonus']
        self.bonus_value = values['bonus_value']
        self.qoe = values['qoe']
        self.qoe_value = values['qoe_value']
        self.technical_value = values['technical_value']
        self.star = values['star']
        self.stared_value = values['stared_value']
        self.time = values['time']


    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `program_elements` WHERE `id` = ? LIMIT 1", (self.id,))
        exists = c.fetchone()

        if not exists:
            c.execute('''INSERT INTO `program_elements` 
                (   `program`, 
                    `box`,
                    `type`, 
                    `label`,
                    `code`,
                    `value_label`,
                    `base_value`,
                    `bonus`,
                    `bonus_value`,
                    `qoe`,
                    `qoe_value`,
                    `technical_value`,
                    `star`,
                    `stared_value`,
                    `time`
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                (
                    self.program, 
                    self.box,
                    self.type, 
                    self.label, 
                    self.code, 
                    self.value_label, 
                    self.base_value, 
                    self.bonus, 
                    self.bonus_value, 
                    self.qoe, 
                    self.qoe_value, 
                    self.technical_value,
                    self.star,
                    self.stared_value,
                    self.time
                ))
            
            # get last id
            c.execute('SELECT `id` FROM `program_elements` ORDER BY `id` DESC LIMIT 1')
            res = c.fetchone()

            self.id = res[0]

        else:
            c.execute('''UPDATE `program_elements` SET 
                            `program` = ?, 
                            `box` = ?,
                            `type` = ?, 
                            `label` = ?,
                            `code` = ?,
                            `value_label` = ?,
                            `base_value` = ?,
                            `bonus` = ?,
                            `bonus_value` = ?,
                            `qoe` = ?,
                            `qoe_value` = ?,
                            `technical_value` = ?,
                            `star` = ?,
                            `stared_value` = ?,
                            `time` = ?
                        WHERE `id` = ?''', (
                            self.program,
                            self.box, 
                            self.type, 
                            self.label, 
                            self.code, 
                            self.value_label, 
                            self.base_value, 
                            self.bonus, 
                            self.bonus_value, 
                            self.qoe, 
                            self.qoe_value, 
                            self.technical_value,
                            self.star,
                            self.stared_value,
                            self.time,
                            self.id
                        ))

        self.conn.commit()

    # Get all values in a dict
    def getAll(self):
        data = {
            'id': self.id,
            'program': self.program,
            'box': self.box,
            'type': self.type,
            'label': self.label,
            'code': self.code,
            'value_label': self.value_label,
            'base_value': self.base_value,
            'bonus': self.bonus,
            'bonus_value': self.bonus_value,
            'qoe': self.qoe,
            'qoe_value': self.qoe_value,
            'technical_value': self.technical_value,
            'star': self.star,
            'stared_value': self.stared_value,
            'time': self.time
        }

        return data

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `program_elements` WHERE `id` = ?', (self.id,))
        self.conn.commit()

    
    # Calculate sum values
    def calculate(self):
        
        # Value autocheck
        if self.value_label == '<<<':
                self.qoe = -3

        self.read()

        # Spin bonus
        bonus = [
            {
                'code': '6R',
                'bv_coef': 0.2,
                'points': 0
            },
            {
                'code': '4R',
                'bv_coef': 0.2,
                'points': 0
            },
            {
                'code': 'DE',
                'bv_coef': 0.15,
                'points': 0
            }
        ]

        if self.code == 'U':
            bonus.append({
                'code': 'Fw',
                'bv_coef': 0,
                'points': 1
            })
            bonus.append({
                'code': 'Ly',
                'bv_coef': 0,
                'points': 1
            })
            bonus.append({
                'code': 'Sw',
                'bv_coef': 0.5,
                'points': 2
            })
            bonus.append({
                'code': 'H',
                'bv_coef': 0.5,
                'points': 0
            })
            bonus.append({
                'code': 'Biel',
                'bv_coef': 0.6,
                'points': 3
            })
            bonus.append({
                'code': 'HBiel',
                'bv_coef': 0.6,
                'points': 4
            })
            bonus.append({
                'code': 'T',
                'bv_coef': 0.4,
                'points': 1
            })
        
        elif self.code == 'S':
            bonus.append({
                'code': 'Sw',
                'bv_coef': 0.6,
                'points': 0
            })
            bonus.append({
                'code': 'Fw',
                'bv_coef': 0.4,
                'points': 0
            })
            bonus.append({
                'code': 'Bh',
                'bv_coef': 0.2,
                'points': 0
            })
        
        elif self.code == 'C':
            bonus.append({
                'code': 'LO',
                'bv_coef': 0.2,
                'points': 0
            })
            bonus.append({
                'code': 'Fw',
                'bv_coef': 0.2,
                'points': 0
            })
            bonus.append({
                'code': 'Sw',
                'bv_coef': 0.2,
                'points': 0
            })

        elif self.code == 'H':
            bonus.append({
                'code': 'LO',
                'bv_coef': 0.3,
                'points': 0
            })
            bonus.append({
                'code': 'Fw',
                'bv_coef': 0.5,
                'points': 0
            })
            bonus.append({
                'code': 'Sw',
                'bv_coef': 0.5,
                'points': 0
            })

        elif self.code == 'In':
            bonus.append({
                'code': 'Bry',
                'bv_coef': 0.25,
                'points': 0
            })

        if self.type == 'CompoSpin':
            bonus.append({
                'code': 'SBC',
                'bv_coef': 0.15,
                'points': 0
            })
            bonus.append({
                'code': 'DCH',
                'bv_coef': 0.15,
                'points': 0
            })
            bonus.append({
                'code': 'BD',
                'bv_coef': 0.2,
                'points': 0
            })

        applied = self.bonus.split(',')

        self.bonus_value = 0

        for bon in bonus:
            if bon['code'] in applied:
                self.bonus_value += (self.base_value * bon['bv_coef']) + bon['points']

        self.bonus_value = round(self.bonus_value, 2)

        # Element value
        self.technical_value = round(self.base_value + self.bonus_value + self.qoe_value, 2)

        if self.technical_value < 0:
            self.technical_value = 0
        
        if self.star:
            self.stared_value = 0

        else:
            self.stared_value = self.technical_value

            if self.time:
                self.stared_value += self.base_value * 0.1
        self.stared_value = round(self.stared_value, 2)

    
    # Read from element table
    def read(self):
        element = Element(self.code)

        if element.code:
            self.label = element.name

            inited = False

            # In case of downgraded, we need to find the element below
            if self.value_label == '<<<':
                rot = self.code[0]
                rot = int(rot) - 1
                if rot == 0:
                    self.base_value = 0
                    inited = True
                else:
                    el = self.code[1:]
                    codeDown = str(rot)+el
                    # Element is replaced by the one bellow both for base value and QOE
                    element = Element(codeDown)
            # End of check downgraded

            
            if not inited:
                # Combo jumb bonus
                if self.type == 'ComboJump':
                    if self.value_label == '<':
                        self.base_value = element.combo_under
                    
                    elif self.value_label == '<<':
                        self.base_value = element.combo_half
                    
                    else:
                        # in the case of <<<, this is the base value of the element bellow
                        self.base_value = element.base_combo
                    # End of check base value
                
                # All other types
                else:
                    if self.value_label == '<':
                        self.base_value = element.under
                    
                    elif self.value_label == '<<':
                        self.base_value = element.half
                    
                    else:
                        # in the case of <<<, this is the base value of the element bellow
                        self.base_value = element.base
                    # End of check base value
                # End of check element type
            # End of check inited

            if self.value_label == '<<<':
                self.qoe = -3

            # QOE reader
            if self.qoe == 3:
                self.qoe_value = element.qoe3
            
            elif self.qoe == 2:
                self.qoe_value = element.qoe2

            elif self.qoe == 1:
                self.qoe_value = element.qoe1

            elif self.qoe == -1:
                self.qoe_value = element.qoem1

            elif self.qoe == -2:
                self.qoe_value = element.qoem2

            elif self.qoe == -3:
                self.qoe_value = element.qoem3

            elif self.qoe == 0:
                self.qoe_value = 0


    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check program_elements table")

        c.execute('''CREATE TABLE IF NOT EXISTS `program_elements`
            (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `program` INTEGER, 
            `box` INTEGER, 
            `type` TEXT, 
            `label` TEXT,
            `code` TEXT,
            `value_label` TEXT,
            `base_value` REAL,
            `bonus` TEXT,
            `bonus_value` REAL,
            `qoe` TEXT,
            `qoe_value` REAL,
            `technical_value` REAL,
            `star` INTEGER,
            `stared_value` REAL,
            `time` INTEGER
            )''')

        c.execute("PRAGMA table_info(`program_elements`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'program': 'INTEGER', 
            'box': 'INTEGER', 
            'type': 'TEXT', 
            'label': 'TEXT',
            'code': 'TEXT',
            'value_label': 'TEXT',
            'base_value': 'REAL',
            'bonus': 'TEXT',
            'bonus_value': 'REAL',
            'qoe': 'TEXT',
            'qoe_value': 'REAL',
            'technical_value': 'REAL',
            'star': 'INTEGER',
            'stared_value': 'REAL',
            'time': 'INTEGER'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `program_elements` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()
