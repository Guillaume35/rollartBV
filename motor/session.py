import sqlite3
import os
from pathlib import Path
import time
import tools
from motor.category import *

class Session:

    def __init__(self, session):

        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        self.conn = sqlite3.connect(db_path)

        session_id = session

        if type(session) is dict:
            data = session

            if 'id' in session:
                session_id = session['id']
            
            else:
                session_id  = 0
            
            self.hydrate(data)

        else:
            c = self.conn.cursor()
            c.row_factory = tools.dict_factory
            c.execute("SELECT * FROM `sessions` WHERE `id` = ? LIMIT 1", (session_id,))

            data = c.fetchone()

            if not data:
                data = {}

            self.hydrate(data)

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'name': 'Unnamed',
            'date': time.strftime('%Y-%m-%d')
        }

        for key in values:
            if key in data:
                values[key] = data[key]

        # hydrate data
        self.name = values['name']
        self.date = values['date']
        self.id = values['id']

    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `sessions` WHERE `id` = ? LIMIT 1", (self.id,))
        exists = c.fetchone()

        if not exists:
            c.execute('INSERT INTO `sessions` (`name`, `date`) VALUES (?,?)', (self.name, self.date))

            # get last id
            c.execute('SELECT `id` FROM `sessions` ORDER BY `id` DESC LIMIT 1')
            res = c.fetchone()

            self.id = res[0]

        else:
            c.execute('UPDATE `sessions` SET `name` = ?, `date` = ? WHERE `id` = ?', (self.name, self.date, self.id))

        self.conn.commit()

    # Get all values in a dict
    def getAll(self):
        data = {
            'id': self.id,
            'name': self.name,
            'date': self.date
        }

        return data

    # Remove element from database
    def delete(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM `sessions` WHERE `id` = ?', (self.id,))
        self.conn.commit()

    def open(self):
        c = self.conn.cursor()

        c.execute('UPDATE `sessions` SET `lock` = "1" WHERE `id` = ?', (self.id,))
        c.execute('UPDATE `sessions` SET `lock` = "0" WHERE `id` != ?', (self.id,))
        self.conn.commit()

    def close(self):
        c = self.conn.cursor()
        c.execute('UPDATE `sessions` SET `lock` = "0"')
        self.conn.commit()

    def getCategories(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM `categories` WHERE `session` = ? ORDER BY `order`, `id`', (self.id, ))
        c.row_factory = tools.dict_factory
        
        data = c.fetchall()

        categories = []

        for d in data:
            categories.append(Category(d))

        return categories

    # get opened session
    @classmethod
    def getOpened(self):
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute('SELECT * FROM `sessions` WHERE `lock` = "1" LIMIT 1')
        data = c.fetchone()

        if data:
            session = self(data)
        
        else:
            session = 0

        conn.close()

        return session

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check sessions table")

        c.execute('''CREATE TABLE IF NOT EXISTS `sessions`
            (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` TEXT,
            `date` TEXT,
            `lock` INTEGER)''')

        c.execute("PRAGMA table_info(`sessions`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'name': 'TEXT',
            'date': 'TEXT',
            'lock': 'INTEGER'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `sessions` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()