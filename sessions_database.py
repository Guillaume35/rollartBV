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
        self.window.geometry("500x720")
        self.window.minsize(480,360)
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