import sqlite3
import os
from pathlib import Path
import tools
from motor.program_element import *

class ProgramBox:

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
            c.execute("SELECT * FROM `program_boxes` WHERE `id` = ? LIMIT 1", (data_id,))

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
            'type': None,
            'order': 0
        }

        for key in values:
            if key in data:
                values[key] = data[key]

        # hydrate data
        self.id = values['id']
        self.program = values['program']
        self.type = values['type']

        if not values['order']:

            c = self.conn.cursor()
            c.row_factory = tools.dict_factory
            c.execute("SELECT * FROM `program_boxes` WHERE `program` = ?", (self.program,))
            boxes = c.fetchall()
            
            self.order = len(boxes) + 1
        
        else:
            self.order = values['order']


    # record data to database
    def record(self):
        c = self.conn.cursor()

        c.row_factory = sqlite3.Row
        c.execute("SELECT * FROM `program_boxes` WHERE `id` = ? LIMIT 1", (self.id,))
        exists = c.fetchone()

        if not exists:
            c.execute('''INSERT INTO `program_boxes` 
                (   `program`, 
                    `type`,
                    `order`
                ) 
                VALUES (?,?,?)''', 
                (
                    self.program, 
                    self.type, 
                    self.order
                ))
            
            # get last id
            c.execute('SELECT `id` FROM `program_boxes` ORDER BY `id` DESC LIMIT 1')
            res = c.fetchone()

            self.id = res[0]

        else:
            c.execute('''UPDATE `program_boxes` SET 
                            `program` = ?, 
                            `type` = ?, 
                            `order` = ?
                        WHERE `id` = ?''', (
                            self.program,
                            self.type,
                            self.order
                        ))

        self.conn.commit()

    # Get all values in a dict
    def getAll(self):
        data = {
            'id': self.id,
            'program': self.program,
            'type': self.type,
            'order': self.order
        }

        return data

    # Get box content
    def getElements(self):
        c = self.conn.cursor()

        c.row_factory = tools.dict_factory
        c.execute("SELECT * FROM `program_elements` WHERE `box` = ? ORDER BY `id`", (self.id, ))

        data = c.fetchall()

        elements = []

        for d in data:
            elements.append(ProgramElement(d))
        
        return elements

    # Empty the box
    def empty(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM `program_elements` WHERE `box` = ?", (self.id, ))
        self.conn.commit()

    # Remove element from database
    def delete(self):
        self.empty()

        order = self.order
        program = self.program

        c = self.conn.cursor()
        c.execute('DELETE FROM `program_boxes` WHERE `id` = ?', (self.id,))
        c.execute("UPDATE `program_boxes` SET `order` = `order` -1 WHERE `order` > ? AND `program` = ?", (order, program))
        self.conn.commit()

    # Create database structure
    @staticmethod
    def database_integrity():
        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)

        c = conn.cursor()

        print ("Check program_boxes table")

        c.execute('''CREATE TABLE IF NOT EXISTS `program_boxes`
            (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `program` INTEGER, 
            `type` TEXT, 
            `order` INTEGER)''')

        c.execute("PRAGMA table_info(`program_boxes`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'program': 'INTEGER', 
            'type': 'TEXT', 
            'order': 'INTEGER'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `program_boxes` ADD COLUMN '%s' '%s'" % (field, type))

        conn.close()
