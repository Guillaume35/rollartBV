import sqlite3
import os
from pathlib import Path
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
            'long_components': 1.0
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
                    `short_components`
                    `long_components`
                ) 
                VALUES (?,?,?,?,?,?,?)''', (self.name, self.order, self.session, self.short, self.long, self.short_components, self.long_components))

        else:
            c.execute('''UPDATE `categories` SET 
                            `name` = ?, 
                            `order` = ?,
                            `session` = ?,
                            ̀`short` = ?,
                            `long` = ?,
                            `short_components` = ?,
                            `long_components` = ? 
                        WHERE `id` = ?''', (self.name, self.order, self.session, self.short, self.long, self.short_components, self.long_components, self.id))

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
            'long_components': self.long_components
        }

        return data

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
            `long_components` REAL)''')

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
            'long_components': 'REAL'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `categories` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()
