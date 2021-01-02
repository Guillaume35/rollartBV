import sqlite3
import os
from pathlib import Path
import time
import tools
from motor.program import *

class Skater:

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
            c.execute("SELECT * FROM `skaters` WHERE `id` = ? LIMIT 1", (data_id,))

            values = c.fetchone()

            if not values:
                values = {}

            self.hydrate(values)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'name': 'unnamed-skater',
            'order': 0,
            'session': 0,
            'category': 0,
            'short_score': 0.0,
            'long_score': 0.0,
            'total_score': 0.0,
            'team': '',
            'status': 'unstarted'
        }

        for key in values:
            if key in data:
                values[key] = data[key]

        # hydrate data
        self.id = values['id']
        self.name = values['name']
        self.order = values['order']
        self.session = values['session']
        self.category = values['category']
        self.short_score = values['short_score']
        self.long_score = values['long_score']
        self.total_score = values['total_score']
        self.team = values['team']
        self.status = values['status']


    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `skaters` WHERE `id` = ? LIMIT 1", (self.id,))
        exists = c.fetchone()

        if not exists:
            c.execute('''INSERT INTO `skaters` 
                (   `name`, 
                    `order`, 
                    `session`,
                    `category`,
                    `short_score`,
                    `long_score`,
                    `total_score`,
                    `team`,
                    `status`
                ) 
                VALUES (?,?,?,?,?,?,?,?,?)''', 
                (
                    self.name, 
                    self.order, 
                    self.session, 
                    self.category, 
                    self.short_score, 
                    self.long_score, 
                    self.total_score, 
                    self.team,
                    self.status
                ))

        else:
            c.execute('''UPDATE `skaters` SET 
                            `name` = ?, 
                            `order` = ?,
                            `session` = ?,
                            `category` = ?,
                            `short_score` = ?,
                            `long_score` = ?,
                            `total_score` = ?,
                            `team` = ?,
                            `status` = ?
                        WHERE `id` = ?''', 
                    (
                        self.name, 
                        self.order, 
                        self.session, 
                        self.category,
                        self.short_score, 
                        self.long_score, 
                        self.total_score, 
                        self.team, 
                        self.status,
                        self.id
                    ))

        self.conn.commit()

    # Get all values in a dict
    def getAll(self):
        data = {
            'id': self.id,
            'name': self.name,
            'order': self.order,
            'session': self.session,
            'category': self.category,
            'short_score': self.short_score,
            'long_score': self.long_score,
            'total_score': self.total_score,
            'team': self.team,
            'status': self.status
        }

        return data

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `skaters` WHERE `id` = ?', (self.id,))
        self.conn.commit()

    def getCurrentProgram(self):

        if self.status.upper() == 'LONG' or self.status.upper() == 'SHORT' or self.status.upper() == 'LONGSTART' or self.status.upper() == 'SHORTSTART':
            c = self.conn.cursor()
            c.row_factory = tools.dict_factory
            c.execute('SELECT * FROM `programs` WHERE `skater_id` = ? AND `program_name` = ? ORDER BY `id` LIMIT 1', (self.id, self.status))
            data = c.fetchone()

            if data:
                program = Program(data)
            else:
                if self.status.upper() == 'SHORT' or self.status.upper() == 'SHORTSTART':
                    progType = 'short'
                else:
                    progType = 'long'

                program = Program({
                    'skater' : self.name,
                    'skater_id' : self.id,
                    'program_name': progType,
                    'category': self.category,
                    'session': self.session
                })
                program.record()

            return program
        else:
            return None

    def calculate(self):
        self.total_score = round(self.short_score + self.long_score, 2)

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check skaters table")

        c.execute('''CREATE TABLE IF NOT EXISTS `skaters`
            (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` TEXT,
            `order` INTEGER,
            `session` INTEGER,
            `category` INTEGER,
            `short_score` REAL,
            `long_score` REAL,
            `total_score` REAL,
            `team` TEXT,
            `status` TEXT)''')

        c.execute("PRAGMA table_info(`skaters`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'name': 'TEXT',
            'order': 'INTEGER',
            'session': 'INTEGER',
            'category': 'INTEGER',
            'short_score': 'REAL',
            'long_score': 'REAL',
            'total_score': 'REAL',
            'team': 'TEXT',
            'status': 'TEXT'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `skaters` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()
