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
                    `category`,
                    `session`,
                    `status`,
                    `fall`
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
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