import sqlite3
from tkinter import *
from motor.session import *
from apps.list import *
import tools

def open_session(session, root):
    sessionOb = Session(session['id'])
    sessionOb.open()
    root.home()

def close_session(sessionOb, root):
    sessionOb.close()
    root.home()

def open_window(root):

    labels = [
        {
            'var': 'name',
            'label': 'Name'
        },
        {
            'var': 'date',
            'label': 'Date'
        }
    ]

    actions = [
        {
            'label': 'Open',
            'action': open_session,
            'params': root
        }
    ]

    # Create main window
    window = Tk()

    # Customizing window
    window.title("Sessions database - RollArt BV")
    window.geometry("500x720")
    window.minsize(480,360)
    window.config(background="#0a1526")

    home_path = str(Path.home())
    db_path = home_path + '/.rollartBV/structure.db'

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.row_factory = tools.dict_factory
    c.execute("SELECT * FROM `sessions` ORDER BY `id` DESC")

    data = c.fetchall()

    list = ListApp(window=window, title="Sessions database", data=data, labels=labels, className=Session, actions=actions)
    list.display()

    # display window
    window.mainloop()

if __name__ == '__main__':
    open_window()
