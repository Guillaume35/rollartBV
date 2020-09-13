import sqlite3
from tkinter import *
from motor.element_type import *
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
