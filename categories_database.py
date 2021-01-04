# Rollart unchained
# Copyright (C) 2021  Free2Skate community

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
from tkinter import *
from apps.list import *
from motor.category import *
import tools

class CategoryApp:

    def __init__(self, parent):
        self.parent = parent
        self.window = None

    def open_window(self):

        labels = [
            {
                'var': 'order',
                'label': 'Order',
                'value': 0
            },
            {
                'var': 'name',
                'label': 'Name',
                'font': 'sans-serif'
            },
            {
                'var': 'short',
                'label': 'Short coef',
                'value': 0.0
            },
            {
                'var': 'long',
                'label': 'Long coef',
                'value': 1.0
            },
            {
                'var': 'short_components',
                'label': 'Short comp. coef',
                'value': 1.0
            },
            {
                'var': 'long_components',
                'label': 'Long comp. coef',
                'value': 1.0
            }
        ]

        default = {
            'session': self.parent.session.id
        }

        # Create main window
        self.window = Tk()

        # Customizing self.window
        self.window.title("Categories database - RollArt BV")
        self.window.geometry("1600x720")
        self.window.minsize(1280,360)
        self.window.config(background="#0a1526")

        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute("SELECT * FROM `categories` WHERE `session` = ? ORDER BY `order`, `id` ASC", (self.parent.session.id,))

        data = c.fetchall()

        list = ListApp(window=self.window, title="Categories database", data=data, labels=labels, className=Category, default=default)
        list.display()

        # display window
        self.window.mainloop()