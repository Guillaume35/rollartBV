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
from motor.skater import *
from motor.program import *
import time
import tools

class Category:

    def __init__(self, data):

        self._type = 'FREESKATING'
        self._status = None
        self._short = 0.0
        self._long = 0.0
        self._compulsory1 = 0.0
        self._compulsory2 = 0.0
        self._style_dance = 0.0
        self._free_dance = 0.0
        self._short_components = 0.0
        self._long_components = 0.0
        self._compulsory_components = 0.0
        self._style_dance_components = 0.0
        self._free_dance_components = 0.0
        self._technical_specialist = ''
        self._controller = ''
        self._assistant = ''
        self._data_operator = ''
        self._judges = 0

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

    @property
    def type(self):
        # Type control
        if self._type not in ['FREESKATING', 'SOLO DANCE']:
            self._type = 'FREESKATING'
        return self._type

    @type.setter
    def type(self, value):
        # Type control
        if value not in ['FREESKATING', 'SOLO DANCE']:
            value = 'FREESKATING'

        if value == 'FREESKATING':
            self.compulsory1 = 0.0
            self.compulsory2 = 0.0
            self.style_dance = 0.0
            self.free_dance = 0.0
        elif value == 'SOLO DANCE':
            self.short = 0.0
            self.long = 0.0
        # End of type control
        
        self._type = value


    @property
    def status(self):

        # Check integrity in case of category type changes
        if self._status and str(self._status).upper() != 'UNSTARTED':
            if self.type == 'FREESKATING' and self._status.upper() not in ('SHORT', 'LONG', 'END'):
                self._status = 'UNSTARTED'
            elif self.type == 'SOLO DANCE' and self._status.upper() not in ('COMPULSORY1', 'COMPULSORY2', 'STYLE_DANCE', 'FREE_DANCE', 'END'):
                self._status = 'UNSTARTED'
        # End of intergrity

        if not self._status or str(self._status).upper() == 'UNSTARTED':
            # For FREESKATING, we only have short or long program.
            # So if status is None, only to case can occure
            if self.type == 'FREESKATING':
                if self.short > 0:
                    self._status = 'SHORT'
                
                else:
                    self._status = 'LONG'

            # For SOLO DANCE, we have to check each possibilities
            elif self.type == 'SOLO DANCE':
                if self.compulsory1 > 0:
                    self._status = 'COMPULSORY1'
                elif self.compulsory2 > 0:
                    self._status = 'COMPULSORY2'
                elif self.style_dance > 0:
                    self._status = 'STYLE_DANCE'
                else:
                    self._status = 'FREE_DANCE'

            else:
                self._status = 'UNSTARTED'
        
        return str(self._status).upper()
    
    @status.setter
    def status(self, value):
        self._status = value

    @property
    def short(self):
        return tools.floatVal(self._short)
    
    @short.setter
    def short(self, value):
        self._short = value
    
    @property
    def long(self):
        return tools.floatVal(self._long)
    
    @long.setter
    def long(self, value):
        self._long = value
    
    @property
    def compulsory1(self):
        return tools.floatVal(self._compulsory1)
    
    @compulsory1.setter
    def compulsory1(self, value):
        self._compulsory1 = value
    
    @property
    def compulsory2(self):
        return tools.floatVal(self._compulsory2)
    
    @compulsory2.setter
    def compulsory2(self, value):
        self._compulsory2 = value

    @property
    def style_dance(self):
        return tools.floatVal(self._style_dance)
    
    @style_dance.setter
    def style_dance(self, value):
        self._style_dance = value
    
    @property
    def free_dance(self):
        return tools.floatVal(self._free_dance)
    
    @free_dance.setter
    def free_dance(self, value):
        self._free_dance = value
    
    @property
    def short_components(self):
        return tools.floatVal(self._short_components)
    
    @short_components.setter
    def short_components(self, value):
        self._short_components = value
    
    @property
    def long_components(self):
        return tools.floatVal(self._long_components)
    
    @long_components.setter
    def long_components(self, value):
        self._long_components = value

    @property
    def compulsory_components(self):
        return tools.floatVal(self._compulsory_components)
    
    @compulsory_components.setter
    def compulsory_components(self, value):
        self._compulsory_components = value
    
    @property
    def style_dance_components(self):
        return tools.floatVal(self._style_dance_components)
    
    @style_dance_components.setter
    def style_dance_components(self, value):
        self._style_dance_components = value
    
    @property
    def free_dance_components(self):
        return tools.floatVal(self._free_dance_components)
    
    @free_dance_components.setter
    def free_dance_components(self, value):
        self._free_dance_components = value
    
    @property
    def technical_specialist(self):
        return tools.stringVal(self._technical_specialist)
    
    @technical_specialist.setter
    def technical_specialist(self, value):
        self._technical_specialist = value

    @property
    def controller(self):
        return tools.stringVal(self._controller)
    
    @controller.setter
    def controller(self, value):
        self._controller = value
    
    @property
    def assistant(self):
        return tools.stringVal(self._assistant)
    
    @assistant.setter
    def assistant(self, value):
        self._assistant = value
    
    @property
    def data_operator(self):
        return tools.stringVal(self._data_operator)
    
    @data_operator.setter
    def data_operator(self, value):
        self._data_operator = value

    @property
    def judges(self):
        self._judges = tools.intVal(self._judges)
        if self._judges < 0:
            self._judges = 0
        return self._judges
    
    @judges.setter
    def judges(self, value):
        value = tools.intVal(value)
        if value < 0:
            value = 0
        self._judges = value

    # Hydrate values to class
    def hydrate(self, data):

        # check data integrity
        values = {
            'id': 0,
            'name': 'Unnamed',
            'order': 0,
            'session': 0,
            'type': 'FREESKATING',
            'short': 0.0,
            'long': 1.0,
            'compulsory1': 0.0,
            'compulsory2': 0.0,
            'style_dance': 0.0,
            'free_dance': 0.0,
            'compulsory1_pattern': None,
            'compulsory2_pattern': None,
            'style_dance_pattern': None,
            'short_components': 1.0,
            'long_components': 1.0,
            'compulsory_components': 1.0,
            'style_dance_components': 1.0,
            'free_dance_components': 1.0,
            'status': 'unstarted',
            'technical_specialist': None,
            'controller': None,
            'assistant': None,
            'data_operator': None,
            'judges': 0
        }

        for key in values:
            if key in data:
                values[key] = data[key]

        # hydrate data
        self.id = values['id']
        self.name = values['name']
        self.order = values['order']
        self.session = values['session']
        self.type = values['type']
        self.short = values['short']
        self.long = values['long']
        self.compulsory1 = values['compulsory1']
        self.compulsory2 = values['compulsory2']
        self.style_dance = values['style_dance']
        self.free_dance = values['free_dance']
        self.compulsory1_pattern = values['compulsory1_pattern']
        self.compulsory2_pattern = values['compulsory2_pattern']
        self.style_dance_pattern = values['style_dance_pattern']
        self.short_components = values['short_components']
        self.long_components = values['long_components']
        self.compulsory_components = values['compulsory_components']
        self.style_dance_components = values['style_dance_components']
        self.free_dance_components = values['free_dance_components']
        self.status = values['status']
        self.technical_specialist = values['technical_specialist']
        self.controller = values['controller']
        self.assistant = values['assistant']
        self.data_operator = values['data_operator']
        self.judges = values['judges']


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
                    `type`,
                    `short`,
                    `long`,
                    `compulsory1`,
                    `compulsory2`,
                    `style_dance`,
                    `free_dance`,
                    `compulsory1_pattern`,
                    `compulsory2_pattern`,
                    `style_dance_pattern`,
                    `short_components`,
                    `long_components`,
                    `compulsory_components`,
                    `style_dance_components`,
                    `free_dance_components`,
                    `status`,
                    `technical_specialist`,
                    `controller`,
                    `assistant`,
                    `data_operator`,
                    `judges`
                ) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                (
                    self.name, 
                    self.order, 
                    self.session, 
                    self.type, 
                    self.short, 
                    self.long, 
                    self.compulsory1, 
                    self.compulsory2, 
                    self.style_dance, 
                    self.free_dance, 
                    self.compulsory1_pattern, 
                    self.compulsory2_pattern, 
                    self.style_dance_pattern, 
                    self.short_components, 
                    self.long_components,
                    self.compulsory_components,
                    self.style_dance_components,
                    self.free_dance_components,
                    self.status,
                    self.technical_specialist,
                    self.controller,
                    self.assistant,
                    self.data_operator,
                    self.judges
                ))
            # get last id
            c.execute('SELECT `id` FROM `categories` ORDER BY `id` DESC LIMIT 1')
            res = c.fetchone()

            self.id = res[0]

        else:
            c.execute('''UPDATE `categories` SET 
                            `name` = ?, 
                            `order` = ?,
                            `session` = ?,
                            `type` = ?,
                            `short` = ?,
                            `long` = ?,
                            `compulsory1` = ?,
                            `compulsory2` = ?,
                            `style_dance` = ?,
                            `free_dance` = ?,
                            `compulsory1_pattern` = ?,
                            `compulsory2_pattern` = ?,
                            `style_dance_pattern` = ?,
                            `short_components` = ?,
                            `long_components` = ?,
                            `compulsory_components` = ?,
                            `style_dance_components` = ?,
                            `free_dance_components` = ?,
                            `status` = ?,
                            `technical_specialist` = ?,
                            `controller` = ?,
                            `assistant` = ?,
                            `data_operator` = ?,
                            `judges` = ?
                        WHERE `id` = ?''', 
                    (
                        
                        self.name, 
                        self.order, 
                        self.session, 
                        self.type, 
                        self.short, 
                        self.long, 
                        self.compulsory1, 
                        self.compulsory2, 
                        self.style_dance, 
                        self.free_dance, 
                        self.compulsory1_pattern, 
                        self.compulsory2_pattern, 
                        self.style_dance_pattern, 
                        self.short_components, 
                        self.long_components, 
                        self.compulsory_components, 
                        self.style_dance_components, 
                        self.free_dance_components, 
                        self.status, 
                        self.technical_specialist,
                        self.controller,
                        self.assistant,
                        self.data_operator,
                        self.judges,
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
            'type': self.type,
            'short': self.short,
            'long': self.long,
            'compulsory1': self.compulsory1,
            'compulsory2': self.compulsory2,
            'style_dance': self.style_dance,
            'free_dance': self.free_dance,
            'compulsory1_pattern': self.compulsory1_pattern,
            'compulsory2_pattern': self.compulsory2_pattern,
            'style_dance_pattern': self.style_dance_pattern,
            'short_components': self.short_components,
            'long_components': self.long_components,
            'compulsory_components': self.compulsory_components,
            'style_dance_components': self.style_dance_components,
            'free_dance_components': self.free_dance_components,
            'status': self.status,
            'technical_specialist': self.technical_specialist,
            'controller': self.controller,
            'assistant': self.assistant,
            'data_operator': self.data_operator,
            'judges': self.judges
        }

        return data

    # Get current skater
    def getCurrentSkater(self):
        c = self.conn.cursor()

        c.row_factory = tools.dict_factory

        # FREESKATING case
        if self.type == 'FREESKATING':
            if self.status == 'SHORT':
                c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "shortend" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                q = True
            elif self.status == 'LONG':
                if self.short > 0:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "longend" ORDER BY `short_score`, `id` LIMIT 1', (self.id, ))
                else:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "longend" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                q = True
        # End of FREESKATING case
        
        # SOLO DANCE case
        elif self.type == 'SOLO DANCE':
            if self.status == 'COMPULSORY1':
                c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "compulsory1end" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                q = True
            elif self.status == 'COMPULSORY2':
                if self.compulsory1 > 0:
                    # Folowing rule need to be applied :
                    # skaters_number / 2. Group 2 goes first, group 1 goes second
                    q = False
                else:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "compulsory2end" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                    q = True
            elif self.status == 'STYLE_DANCE':
                if self.compulsory1 > 0 or self.compulsory2 > 0:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "style_danceend" ORDER BY `compulsory_score`, `id` LIMIT 1', (self.id, ))
                else:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "style_danceend" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                q = True
            elif self.status == 'FREE_DANCE':
                if self.style_dance > 0:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "free_danceend" ORDER BY `style_dance_score`, `id` LIMIT 1', (self.id, ))
                elif self.compulsory1 > 0 or self.compulsory2 > 0:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "free_danceend" ORDER BY `compulsory_score`, `id` LIMIT 1', (self.id, ))
                else:
                    c.execute('SELECT * FROM `skaters` WHERE `category` = ? AND `status` NOT LIKE "free_danceend" ORDER BY `order`, `id` LIMIT 1', (self.id, ))
                q = True
        # End of SOLO DANCE case
        
        if q:
            data = c.fetchone()
            
            if data:
                return Skater(data)
            else:
                return None
        
        else:
            return None

    # Get all skaters in category
    def getSkaters(self, orderby="order"):

        # define order by statement
        if orderby == 'current':
            if self.type == 'FREESKATING':
                # Order by order for short program
                if self.status in ('SHORT', 'UNSTARTED'):
                    orderby = 'order'
                # Long program status, order by short results or by order if no short
                else:
                    if self.short > 0:
                        orderby = 'short'
                    else:
                        orderby = 'order'
            # End of Freeskating statement

            # Solo dance statement
            elif self.type == 'SOLO DANCE':
                # Orderby order for compulsory and unstarted status
                if self.status in ('COMPULSORY1', 'COMPULSORY2', 'UNSTARTED'):
                    orderby = 'order'
                # Style dance order by compulsory if exists or order
                elif self.status == 'STYLE_DANCE':
                    if self.compulsory1 > 0 or self.compulsory2 > 0:
                        orderby = 'compulsory_score'
                    else:
                        orderby = 'order'
                # Free dance order by style dance if exists, compulsory if exists or order
                elif self.status in ('FREE_DANCE', 'END'):
                    if self.style_dance > 0:
                        orderby = 'style_dance_score'
                    elif self.compulsory1 > 0 or self.compulsory2 > 0:
                        orderby = 'compulsory_score'
                    else:
                        orderby = 'order'
        # End of order by statement

        c = self.conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute('SELECT * FROM `skaters` WHERE `category` = ? ORDER BY ?, `id`', (self.id, orderby))
        data = c.fetchall()

        skaters = []

        for d in data:
            skaters.append(Skater(d))

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

    # reset
    def reset(self):
        self.status = "UNSTARTED"
        self.record()

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
            `order` INTEGER,
            `session` INTEGER,
            `type` TEXT,
            `short` REAL,
            `long` REAL,
            `compulsory1` REAL,
            `compulsory2` REAL,
            `style_dance` REAL,
            `free_dance` REAL,
            `compulsory1_pattern` TEXT,
            `compulsory2_pattern` TEXT,
            `style_dance_pattern` TEXT,
            `short_components` REAL,
            `long_components` REAL,
            `compulsory_components` REAL,
            `style_dance_components` REAL,
            `free_dance_components` REAL,
            `status` TEXT,
            `technical_specialist` TEXT
            `controller` TEXT
            `assistant` TEXT
            `data_operator` TEXT
            `judges` TEXT)''')

        c.execute("PRAGMA table_info(`categories`)")
        fields = c.fetchall()

        existing = []

        for field in fields:
            existing.append(field[1])

        fields = {
            'name': 'TEXT',
            'order': 'INTEGER',
            'session': 'INTEGER',
            'type': 'TEXT',
            'short': 'REAL',
            'long': 'REAL',
            'compulsory1': 'REAL',
            'compulsory2': 'REAL',
            'style_dance': 'REAL',
            'free_dance': 'REAL',
            'compulsory1_pattern': 'TEXT',
            'compulsory2_pattern': 'TEXT',
            'style_dance_pattern': 'TEXT',
            'short_components': 'REAL',
            'long_components': 'REAL',
            'compulsory_components': 'REAL',
            'style_dance_components': 'REAL',
            'free_dance_components': 'REAL',
            'status': 'TEXT',
            'technical_specialist': 'TEXT',
            'controller': 'TEXT',
            'assistant': 'TEXT',
            'data_operator': 'TEXT',
            'judges': 'TEXT'
        }

        for field, type in fields.items():
            if not field in existing:
                print ("Add "+field+" "+type+" to table")
                c.execute("ALTER TABLE `categories` ADD COLUMN '%s' '%s'" % (field, type))

                # # Set type of all created categories to FREESKATING
                # # There is a bug here
                # if field == 'type':
                #    print ("Make all categories types to FREESKATING (compatibility issue)")
                #    c.execute("UPDATE `categories` SET `type` = 'FREESKATING'")

        conn.close()
