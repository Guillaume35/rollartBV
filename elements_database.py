import sqlite3
from tkinter import *
from apps.list import *
from motor.element import *

def open_window():

    labels = [
        {
            'var': 'name',
            'label': 'Name',
            'width': 15,
            'font': 'sans-serif'
        },
        {
            'var': 'code',
            'label': 'Code',
            'width': 10,
            'font': 'sans-serif'
        },
        {
            'var': 'qoe3',
            'label': '+3'
        },
        {
            'var': 'qoe2',
            'label': '+2'
        },
        {
            'var': 'qoe1',
            'label': '+1'
        },
        {
            'var': 'base',
            'label': 'BASE'
        },
        {
            'var': 'under',
            'label': '<'
        },
        {
            'var': 'half',
            'label': '<<'
        },
        {
            'var': 'down',
            'label': '<<<'
        },
        {
            'var': 'qoem1',
            'label': '-1'
        },
        {
            'var': 'qoem2',
            'label': '-2'
        },
        {
            'var': 'qoem3',
            'label': '-3'
        },
        {
            'var': 'base_combo',
            'label': 'COMBO'
        },
        {
            'var': 'combo_under',
            'label': 'Comb<'
        },
        {
            'var': 'combo_half',
            'label': 'Comb<<'
        },
        {
            'var': 'combo_down',
            'label': 'Comb<<<'
        },
        {
            'var': 'type',
            'label': 'Type'
        }
    ]

    # Create main window
    window = Tk()

    # Customizing window
    window.title("Elements database - RollArt BV")
    window.geometry("1280x720")
    window.minsize(480,360)
    window.config(background="#0a1526")

    home_path = str(Path.home())
    db_path = home_path + '/.rollartBV/structure.db'

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.row_factory = sqlite3.Row
    c.execute("SELECT * FROM `elements` ORDER BY `code`")

    data = c.fetchall()

    list = ListApp(window=window, title="Elements database", data=data, labels=labels, className=Element)
    list.display()

    # display window
    window.mainloop()

if __name__ == '__main__':
    open_window()
