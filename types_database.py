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
from apps.list import *

def open_window():

    labels = [
        {
            'var': 'name',
            'label': 'Name'
        },
        {
            'var': 'code',
            'label': 'code'
        }
    ]

    # Create main window
    window = Tk()

    # Customizing window
    window.title("Types database - RollArt BV")
    window.geometry("500x720")
    window.minsize(480,360)
    window.config(background="#0a1526")

    home_path = str(Path.home())
    db_path = home_path + '/.rollartBV/structure.db'

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.row_factory = sqlite3.Row
    c.execute("SELECT * FROM `elements_types` ORDER BY `name`")

    data = c.fetchall()

    list = ListApp(window=window, title="Types database", data=data, labels=labels, className=ElementType)
    list.display()

    # display window
    window.mainloop()

if __name__ == '__main__':
    open_window()
