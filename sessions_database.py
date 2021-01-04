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
from tkinter import *
from motor.session import *
from apps.list import *
import tools

class SessionApp:

    def __init__(self, parent):
        self.parent = parent
        self.window = None

    def open_session(self, session):
        sessionOb = Session(session['id'])
        sessionOb.open()
        self.parent.session = sessionOb
        self.parent.home()
        self.window.destroy()
    
    def close_session(self, sessionOb):
        sessionOb.close()
        self.parent.session = None
        self.parent.home()

    def open_window(self):

        labels = [
            {
                'var': 'name',
                'label': 'Name',
                'font': 'sans-serif'
            },
            {
                'var': 'date',
                'label': 'Date'
            }
        ]

        actions = [
            {
                'label': 'Open',
                'action': self.open_session
            }
        ]

        # Create main window
        self.window = Tk()

        # Customizing self.window
        self.window.title("Sessions database - RollArt BV")
        self.window.geometry("900x720")
        self.window.minsize(500,360)
        self.window.config(background="#0a1526")

        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute("SELECT * FROM `sessions` ORDER BY `id` DESC")

        data = c.fetchall()

        list = ListApp(window=self.window, title="Sessions database", data=data, labels=labels, className=Session, actions=actions)
        list.display()

        # display window
        self.window.mainloop()