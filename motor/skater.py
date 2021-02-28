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
from motor.program import *

class Skater:

    def __init__(self, data):

        self._short_score = 0.0
        self._long_score = 0.0
        self._compulsory_score = 0.0
        self._style_dance_score = 0.0
        self._free_dance_score = 0.0
        self._status = 'UNSTARTED'

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
    
    @property
    def short_score(self):
        return self._short_score

    @short_score.setter
    def short_score(self, value):
        self._short_score = tools.floatVal(value)
    
    @property
    def long_score(self):
        return self._long_score

    @long_score.setter
    def long_score(self, value):
        self._long_score = tools.floatVal(value)

    @property
    def compulsory_score(self):
        return self._compulsory_score

    @compulsory_score.setter
    def compulsory_score(self, value):
        self._compulsory_score = tools.floatVal(value)

    @property
    def style_dance_score(self):
        return self._style_dance_score
        
    @style_dance_score.setter
    def style_dance_score(self, value):
        self._style_dance_score = tools.floatVal(value)

    @property
    def free_dance_score(self):
        return self._free_dance_score
        
    @free_dance_score.setter
    def free_dance_score(self, value):
        self._free_dance_score = tools.floatVal(value)

    @property
    def status(self):
        return self._status
        
    @status.setter
    def status(self, value):
        if not value:
            value = ''
        self._status = value.upper()

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'name': 'unnamed-skater',
            'order': 0,
            'session': 0,
            'category': 0,
            'initial_score': 0.0,
            'short_score': 0.0,
            'long_score': 0.0,
            'compulsory_score': 0.0,
            'style_dance_score': 0.0,
            'free_dance_score': 0.0,
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
        self.initial_score = values['initial_score']
        self.short_score = values['short_score']
        self.long_score = values['long_score']
        self.compulsory_score = values['compulsory_score']
        self.style_dance_score = values['style_dance_score']
        self.free_dance_score = values['free_dance_score']
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
                    `initial_score`,
                    `short_score`,
                    `long_score`,
                    `compulsory_score`,
                    `style_dance_score`,
                    `free_dance_score`,
                    `total_score`,
                    `team`,
                    `status`
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                (
                    self.name, 
                    self.order, 
                    self.session, 
                    self.category, 
                    self.initial_score,
                    self.short_score, 
                    self.long_score, 
                    self.compulsory_score, 
                    self.style_dance_score, 
                    self.free_dance_score, 
                    self.total_score, 
                    self.team,
                    self.status
                ))

            # get last id
            c.execute('SELECT `id` FROM `skaters` ORDER BY `id` DESC LIMIT 1')
            res = c.fetchone()

            self.id = res[0]

        else:
            c.execute('''UPDATE `skaters` SET 
                            `name` = ?, 
                            `order` = ?,
                            `session` = ?,
                            `category` = ?,
                            `initial_score` = ?,
                            `short_score` = ?,
                            `long_score` = ?,
                            `compulsory_score` = ?,
                            `style_dance_score` = ?,
                            `free_dance_score` = ?,
                            `total_score` = ?,
                            `team` = ?,
                            `status` = ?
                        WHERE `id` = ?''', 
                    (
                        self.name, 
                        self.order, 
                        self.session, 
                        self.category,
                        self.initial_score,
                        self.short_score, 
                        self.long_score, 
                        self.compulsory_score, 
                        self.style_dance_score, 
                        self.free_dance_score, 
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
            'initial_score': self.initial_score,
            'short_score': self.short_score,
            'long_score': self.long_score,
            'compulsory_score': self.compulsory_score,
            'style_dance_score': self.style_dance_score,
            'free_dance_score': self.free_dance_score,
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

    # Get the opened program of the skater or return none
    def getCurrentProgram(self):

        # Skater is not over
        if self.status in ['LONG', 'SHORT', 'LONGSTART', 'SHORTSTART', 'COMPULSORY1', 'COMPULSORY1START', 'COMPULSORY2', 'COMPULSORY2START', 'STYLE_DANCE', 'STYLE_DANCESTART', 'FREE_DANCE', 'FREE_DANCESTART']:
            c = self.conn.cursor()
            c.row_factory = tools.dict_factory
            c.execute('SELECT * FROM `programs` WHERE `skater_id` = ? AND `program_name` LIKE ? ORDER BY `id` LIMIT 1', (self.id, self.status))
            data = c.fetchone()

            # Program is currently started
            if data:
                program = Program(data)

            # Start and record the program
            else:
                if self.status in ['SHORT', 'SHORTSTART']:
                    progType = 'short'
                elif self.status in ['LONG', 'LONGSTART']:
                    progType = 'long'
                elif self.status in ['COMPULSORY1', 'COMPULSORY1START']:
                    progType = 'compulsory1'
                elif self.status in ['COMPULSORY2', 'COMPULSORY2START']:
                    progType = 'compulsory2'
                elif self.status in ['STYLE_DANCE', 'STYLE_DANCESTART']:
                    progType = 'style_dance'
                elif self.status in ['FREE_DANCE', 'FREE_DANCESTART']:
                    progType = 'free_dance'

                program = Program({
                    'skater' : self.name,
                    'skater_id' : self.id,
                    'program_name': progType,
                    'category': self.category,
                    'session': self.session
                })
                program.record()

            return program
        
        # No more program for this skater
        else:
            return None

    def calculate(self):
        initial_score = 0
        if self.initial_score:
            initial_score = float(self.initial_score)

        self.total_score = round(self.short_score + self.long_score + self.compulsory_score + self.style_dance_score + self.free_dance_score + initial_score, 2)

    def getTeamScore(self):
        c = self.conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute('SELECT SUM(`total_score`) AS `sum` FROM `skaters` WHERE `session` = ? AND `team` LIKE ?', (self.session, self.team))
        data = c.fetchone()

        if data:
            score = data['sum']
        else:
            score = 0

        return score

    # get all teams
    @staticmethod
    def getTeams(session):
        conn = tools.getDb()
        c = conn.cursor()

        c.row_factory = tools.dict_factory
        c.execute('SELECT `team`, SUM(`total_score`) AS `total_score` FROM `skaters` WHERE `session` = ? GROUP BY `team`', (session,))
        data = c.fetchall()

        if data:
            teams = data
        else:
            teams = None

        return teams

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
            `initial_score` REAL,
            `short_score` REAL,
            `long_score` REAL,
            `compulsory_score` REAL,
            `style_dance_score` REAL,
            `free_dance_score` REAL,
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
            'initial_score' : 'REAL',
            'short_score': 'REAL',
            'long_score': 'REAL',
            'compulsory_score': 'REAL',
            'style_dance_score': 'REAL',
            'free_dance_score': 'REAL',
            'total_score': 'REAL',
            'team': 'TEXT',
            'status': 'TEXT'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `skaters` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()
