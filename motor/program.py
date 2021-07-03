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
import time
import tools
from motor.program_box import *
from motor.program_element import *

class Program:

    def __init__(self, data):

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
            c.execute("SELECT * FROM `programs` WHERE `id` = ? LIMIT 1", (data_id,))

            values = c.fetchone()

            if not values:
                values = {}

            self.hydrate(values)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'skater': 'unamed-skater',
            'skater_id': 0,
            'program_name': 'long',
            'start': 0,
            'end': 0,
            'duration': 0,
            'technical_score': 0.0,
            'skating_skills': 0.0,
            'transitions': 0.0,
            'performance': 0.0,
            'choreography': 0.0,
            'components_coef': 1.0,
            'components_score': 0.0,
            'program_value': 0.0,
            'penalization': 0.0,
            'score': 0.0,
            'total_score': 0.0,
            'category': 0,
            'session': 0,
            'status': 'start',
            'fall': 0
        }

        for key in values:
            if key in data:
                values[key] = data[key]

        # hydrate data
        self.id = values['id']
        self.skater = values['skater']
        self.skater_id = values['skater_id']
        self.program_name = values['program_name']
        self.start = values['start']
        self.end = values['end']
        self.duration = values['duration']
        self.technical_score = values['technical_score']
        self.skating_skills = values['skating_skills']
        self.transitions = values['transitions']
        self.performance = values['performance']
        self.choreography = values['choreography']
        self.components_coef = values['components_coef']
        self.components_score = values['components_score']
        self.program_value = values['program_value']
        self.penalization = values['penalization']
        self.score = values['score']
        self.total_score = values['total_score']
        self.category = values['category']
        self.session = values['session']
        self.status = values['status']
        self.fall = values['fall']


    
    # Get program content
    def getElements(self):
        c = self.conn.cursor()

        c.row_factory = tools.dict_factory
        c.execute("SELECT * FROM `program_elements` WHERE `program` = ? ORDER BY `id`", (self.id, ))

        data = c.fetchall()

        elements = []

        for d in data:
            elements.append(ProgramElement(d))
        
        return elements

    # Get program content
    def getBoxes(self):
        c = self.conn.cursor()

        c.row_factory = tools.dict_factory
        c.execute("SELECT * FROM `program_boxes` WHERE `program` = ? ORDER BY `order`, `id`", (self.id, ))

        data = c.fetchall()

        boxes = []

        for d in data:
            boxes.append(ProgramBox(d))
        
        return boxes

    # calculate program value
    def calculate(self):
        c = self.conn.cursor()

        c.execute("SELECT SUM(`stared_value`) FROM `program_elements` WHERE `program` = ?", (self.id, ))

        data = c.fetchone()

        if data[0]:
            val = data[0]
        else:
            val = 0

        self.technical_score = round(val, 2)
        self.components_score = round((self.skating_skills + self.transitions + self.choreography + self.performance) * self.components_coef, 2)
        self.program_value = round(self.technical_score + self.components_score, 2)
        self.score = round(self.program_value + self.penalization, 2)

        if self.score < 0:
            self.score = 0
        
        self.total_score = self.score

        last_program = False

        # Calculate the total score in case
        # First competition mode check
        if self.skater_id and self.category:

            c.row_factory = tools.dict_factory

            # Secondly, get category configuration

            c.execute("SELECT * FROM `categories` WHERE `id` = ?", (self.category, ))
            category = c.fetchone()

            # Freeskating case
            if category['type'].upper() == 'FREESKATING':

                # In freeskating mode, the last program is long program
                if self.program_name.upper() == 'LONG':

                    last_program = True

                    # Add short program score if activated
                    if category['short']:
                        c.execute("SELECT * FROM `programs` WHERE `program_name` LIKE 'short' AND `skater_id` = ? AND `category` = ? AND `session` = ? LIMIT 1", 
                            (self.skater_id, self.category, self.session))

                        data = c.fetchone()

                        if data:
                            self.total_score += data['score']
            # End of freeskating statement

            # Solo dance case
            elif category['type'].upper() == 'SOLO DANCE':

                # In SOLO DANCE mode, last program can be COMPULSORY1, COMPULSORY2 or FREE_DANCE
                cond = (self.skater_id, self.category, self.session)
                data = None

                if category['free_dance'] and self.program_name.upper() == 'FREE_DANCE':
                    query = "SELECT SUM(`score`) AS `total` FROM `programs` WHERE UPPER(`program_name`) IN ('STYLE_DANCE', 'COMPULSORY2', 'COMPULSORY1') AND `skater_id` = ? AND `category` = ? AND `session` = ? LIMIT 1"
                    c.execute(query, cond)
                    data = c.fetchone()
                    last_program = True
                
                elif category['style_dance'] and self.program_name.upper() == 'STYLE_DANCE':
                    query = "SELECT SUM(`score`) AS `total` FROM `programs` WHERE UPPER(`program_name`) IN ('COMPULSORY2', 'COMPULSORY1') AND `skater_id` = ? AND `category` = ? AND `session` = ? LIMIT 1"
                    c.execute(query, cond)
                    data = c.fetchone()
                    last_program = True

                elif category['compulsory2'] and self.program_name.upper() == 'COMPULSORY2':
                    query = "SELECT SUM(`score`) AS `total` FROM `programs` WHERE UPPER(`program_name`) IN ('COMPULSORY1') AND `skater_id` = ? AND `category` = ? AND `session` = ? LIMIT 1"
                    c.execute(query, cond)
                    data = c.fetchone()
                    last_program = True

                elif category['compulsory1'] and self.program_name.upper() == 'COMPULSORY1':
                    last_program = True


                if data:
                    if data['total']:
                        self.total_score += float(data['total'])
            # End of solo dance statement

        # Add initial score in case of it is the last program
        if last_program:
            c.execute("SELECT `initial_score` FROM `skaters` WHERE `id` = ?", (self.skater_id, ))
            data = c.fetchone()

            if data['initial_score']:
                self.total_score += float(data['initial_score'])
        # End of last program statement
        
        self.total_score = round(self.total_score, 2)


    # get rank for this program
    def getRank(self):
        c = self.conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute("SELECT COUNT(*) AS `num` FROM `programs` WHERE `total_score` > ? AND `category` = ? AND `program_name` = ? AND `id` != ?", (self.total_score, self.category, self.program_name, self.id))
        data = c.fetchone()

        if data:
            rank = data['num'] + 1
        else:
            rank = 1
        
        return rank

    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `programs` WHERE `id` = ? LIMIT 1", (self.id,))
        exists = c.fetchone()

        if not exists:
            c.execute('''INSERT INTO `programs` 
                (   `skater`, 
                    `skater_id`, 
                    `program_name`,
                    `start`,
                    `end`,
                    `duration`,
                    `technical_score`,
                    `penalization`,
                    `skating_skills`,
                    `transitions`,
                    `performance`,
                    `choreography`,
                    `components_coef`,
                    `components_score`,
                    `program_value`,
                    `score`,
                    `total_score`,
                    `category`,
                    `session`,
                    `status`,
                    `fall`
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                (
                    self.skater, 
                    self.skater_id, 
                    self.program_name, 
                    self.start, 
                    self.end, 
                    self.duration, 
                    self.technical_score, 
                    self.penalization, 
                    self.skating_skills, 
                    self.transitions,
                    self.performance,
                    self.choreography,
                    self.components_coef,
                    self.components_score,
                    self.program_value,
                    self.score,
                    self.total_score,
                    self.category,
                    self.session,
                    self.status,
                    self.fall
                ))
            
            # get last id
            c.execute('SELECT `id` FROM `programs` ORDER BY `id` DESC LIMIT 1')
            res = c.fetchone()

            self.id = res[0]

        else:
            c.execute('''UPDATE `programs` SET 
                            `skater` = ?, 
                            `skater_id` = ?, 
                            `program_name` = ?,
                            `start` = ?,
                            `end` = ?,
                            `duration` = ?,
                            `technical_score` = ?,
                            `penalization` = ?,
                            `skating_skills` = ?,
                            `transitions` = ?,
                            `performance` = ?,
                            `choreography` = ?,
                            `components_coef` = ?,
                            `components_score` = ?,
                            `program_value` = ?,
                            `score` = ?,
                            `total_score` = ?,
                            `category` = ?,
                            `session` = ?,
                            `status` = ?,
                            `fall` = ?
                        WHERE `id` = ?''', (
                            self.skater, 
                            self.skater_id, 
                            self.program_name, 
                            self.start, 
                            self.end, 
                            self.duration, 
                            self.technical_score, 
                            self.penalization, 
                            self.skating_skills, 
                            self.transitions,
                            self.performance,
                            self.choreography,
                            self.components_coef,
                            self.components_score,
                            self.program_value,
                            self.score,
                            self.total_score,
                            self.category,
                            self.session,
                            self.status,
                            self.fall,
                            self.id
                        ))

        self.conn.commit()

    # Get all values in a dict
    def getAll(self):
        data = {
            'id': self.id,
            'skater': self.skater,
            'skater_id': self.skater_id,
            'program_name': self.program_name,
            'start': self.start,
            'end': self.end,
            'duration': self.duration,
            'technical_score': self.technical_score,
            'skating_skills': self.skating_skills,
            'transitions': self.transitions,
            'performance': self.performance,
            'choreography': self.choreography,
            'components_coef': self.components_coef,
            'components_score': self.components_score,
            'program_value': self.program_value,
            'penalization': self.penalization,
            'score': self.score,
            'total_score': self.total_score,
            'category': self.category,
            'session': self.session,
            'status': self.status,
            'fall': self.fall
        }

        return data

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `programs` WHERE `id` = ?', (self.id,))
        self.conn.commit()

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check programs table")

        c.execute('''CREATE TABLE IF NOT EXISTS `programs`
            (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `skater` TEXT, 
            `skater_id` INTEGER, 
            `program_name` TEXT,
            `start` INTEGER,
            `end` INTEGER,
            `duration` INTEGER,
            `technical_score` REAL,
            `skating_skills` REAL,
            `transitions` REAL,
            `performance` REAL,
            `choreography` REAL,
            `components_coef` REAL,
            `components_score` REAL,
            `program_value` REAL,
            `penalization` REAL,
            `score` REAL,
            `total_score` REAL,
            `category` INTEGER,
            `session` INTEGER,
            `status` TEXT,
            `fall` INTEGER)''')

        c.execute("PRAGMA table_info(`programs`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'skater': 'TEXT', 
            'skater_id': 'INTEGER', 
            'program_name': 'TEXT',
            'start': 'INTEGER',
            'end': 'INTEGER',
            'duration': 'INTEGER',
            'technical_score': 'REAL',
            'skating_skills': 'REAL',
            'transitions': 'REAL',
            'performance': 'REAL',
            'choreography': 'REAL',
            'components_coef': 'REAL',
            'components_score': 'REAL',
            'program_value': 'REAL',
            'penalization': 'REAL',
            'score': 'REAL',
            'total_score': 'REAL',
            'category': 'INTEGER',
            'session': 'INTEGER',
            'status': 'TEXT',
            'fall': 'INTEGER'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `programs` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()