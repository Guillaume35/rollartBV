import sqlite3
import os
from pathlib import Path
from motor.skater import *
from motor.program import *
import time
import tools

class Category:

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
            c.execute("SELECT * FROM `categories` WHERE `id` = ? LIMIT 1", (data_id,))

            values = c.fetchone()

            if not values:
                values = {}

            self.hydrate(values)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'name': 'Unnamed',
            'order': 0,
            'session': 0,
            'short': 0.0,
            'long': 1.0,
            'short_components': 1.0,
            'long_components': 1.0,
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
        self.short = values['short']
        self.long = values['long']
        self.short_components = values['short_components']
        self.long_components = values['long_components']
        self.status = values['status']


    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `categories` WHERE `id` = ? LIMIT 1", (self.id,))
        exists = c.fetchone()

        if not exists:
            c.execute('''INSERT INTO `categories` 
                (   `name`, 
                    `order`, 
                    `session`,
                    `short`,
                    `long`,
                    `short_components`,
                    `long_components`,
                    `status`
                ) 
                VALUES (?,?,?,?,?,?,?,?)''', 
                (
                    self.name, 
                    self.order, 
                    self.session, 
                    self.short, 
                    self.long, 
                    self.short_components, 
                    self.long_components,
                    self.status
                ))

        else:
            c.execute('''UPDATE `categories` SET 
                            `name` = ?, 
                            `order` = ?,
                            `session` = ?,
                            `short` = ?,
                            `long` = ?,
                            `short_components` = ?,
                            `long_components` = ?,
                            `status` = ?
                        WHERE `id` = ?''', 
                    (
                        
                        self.name, 
                        self.order, 
                        self.session, 
                        self.short, 
                        self.long, 
                        self.short_components, 
                        self.long_components, 
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
            'short': self.short,
            'long': self.long,
            'short_components': self.short_components,
            'long_components': self.long_components,
            'status': self.status
        }

        return data

    def getCurrentSkater(self):
        c = self.conn.cursor()

        c.row_factory = tools.dict_factory

        if str(self.status).upper() == 'UNSTARTED' or not self.status:
            if self.short > 0:
                self.status = 'short'
            else:
                self.status = 'long'
            
            self.record()

        if self.status.upper() == 'SHORT':
            c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` != "shortend" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
            q = True
        elif self.status.upper() == 'LONG':
            if self.short > 0:
                c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` != "longend" ORDER BY `short_score`, `id` LIMIT 1', (self.id, ))
                q = True
            else:
                c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` != "longend" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                q = True
        
        if q:
            data = c.fetchone()

            print(self.id)
            
            if data:
                return Skater(data)
            else:
                return None
        
        else:
            return None

    # Get all skaters in category
    def getSkaters(self):
        c = self.conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute('SELECT * FROM `skaters` WHERE `category` = ? ORDER BY `order`, `id`', (self.id, ))
        data = c.fetchall()

        skaters = []

        for d in data:
            skaters.append(Skater(data))

        return skaters

    # Count skaters
    def getSkatersNum(self):
        c = self.conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute('SELECT COUNT(*) AS `num` FROM `skaters` WHERE `category` = ?', (self.id, ))
        data = c.fetchone()

        return data['num']

    # get results
    def getResults(self, program_name):
        c = self.conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute('SELECT * FROM `programs` WHERE `category` = ? AND `program_name` = ? ORDER BY `total_score` DESC, `components_score` DESC', (self.id, program_name))
        data = c.fetchall()

        programs = []

        for d in data:
            programs.append(Program(d))

        return programs

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `categories` WHERE `id` = ?', (self.id,))
        self.conn.commit()

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check categories table")

        c.execute('''CREATE TABLE IF NOT EXISTS `categories`
            (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` TEXT,
            `order` TEXT,
            `session` INTEGER,
            `short` REAL,
            `long` REAL,
            `short_components` REAL,
            `long_components` REAL,
            `status` TEXT)''')

        c.execute("PRAGMA table_info(`categories`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'name': 'TEXT',
            'order': 'TEXT',
            'session': 'INTEGER',
            'short': 'REAL',
            'long': 'REAL',
            'short_components': 'REAL',
            'long_components': 'REAL',
            'status': 'TEXT'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `categories` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()
