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

    """
    * Application for category creation and configuration.
    * First manager has to configure a categoy with a name and type.
    * Then, config button is available to toggle programs and components coef
    * depending on category type (FREESKATING, SOLO DANCE...)
    """

    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.frame = None
        self.category = None

        self.shortVar = None
        self.longVar = None
        self.shortCompoEntry = None
        self.longCompoEntry = None

        self.compulsory1Var = None
        self.compulsory2Var = None
        self.style_danceVar = None
        self.free_danceVar = None
        self.compulsoryCompoEntry = None
        self.style_danceCompoEntry = None
        self.free_danceCompoEntry = None
        self.compulsory1DanceVar = None
        self.compulsory2DanceVar = None
        self.style_dancePatternVar = None
        self.statusVar = None

    def open_window(self):

        # Create main window
        self.window = Toplevel(self.parent.window) # Tk()

        # Customizing self.window
        self.window.title("Categories database - RollArt BV")
        self.window.geometry("1600x720")
        self.window.minsize(1280,360)
        self.window.config(background="#0a1526")

        self.list()

        # display window
        self.window.mainloop()

    #
    # list()
    # Load categories list and basic configuration options
    def list(self):

        # clear root window
        for c in self.window.winfo_children():
            c.destroy()

        home_path = str(Path.home())
        db_path = home_path + '/.rollartBV/structure.db'

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute("SELECT * FROM `categories` WHERE `session` = ? ORDER BY `order` ASC, `id` ASC", (self.parent.session.id,))

        data = c.fetchall()

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
                'var': 'type',
                'label': 'Type',
                'value': 'FREESKATING',
                'type': 'OptionMenu',
                'options': ('FREESKATING', 'SOLO DANCE')
            }
        ]

        actions = [
            {
                'label': 'Config',
                'action': self.config
            }
        ]

        default = {
            'session': self.parent.session.id
        }

        list = ListApp(window=self.window, title="Categories database", data=data, labels=labels, className=Category, default=default, actions=actions)
        list.display()
    # End of list()


    #
    # config(category = Dict)
    # Load configuration panel in window. This configuration panel should show the interface 
    # depending on the category global configuration : freeskating, solo dance, couple dance, pairs...
    def config(self, category):
        
        # clear root window
        for c in self.window.winfo_children():
            c.destroy()

        self.frame = Frame(self.window, bg="#0a1526")

        self.category = Category(category)

        # Title frame

        title_frame = Frame(self.frame, bg="#bd3800")

        btn = Button(title_frame, text="Cancel", font=("sans-serif", 12), command=self.list)
        btn.grid(row=0, column=0, sticky="nsew")

        # check category type
        if not self.category.type:
            self.category.type = 'FREESKATING'

        label = Label(title_frame, text=self.category.name+" ("+self.category.type+")", font=("sans-serif", 14), fg="white", bg="#bd3800")
        label.grid(row=0, column=1, sticky="nsw", padx="10")

        btn = Button(title_frame, text="Save", font=("sans-serif", 12), bg="green", fg="white", command=self.record)
        btn.grid(row=0, column=2, sticky="nsew")

        Grid.columnconfigure(title_frame, 1, weight=1)

        title_frame.pack(fill=X)

        # Form depending on which competition type is selected
        frame = Frame(self.frame, bg="#0a1526")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        i = 0

        label = Label(frame, text="Option", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
        label.grid(row=0, column=i, pady=10, sticky="w")
        i += 1

        if self.category.type == "SOLO DANCE":
            label = Label(frame, text="Pattern", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
            label.grid(row=0, column=i, pady=10, sticky="w")
            i += 1

        label = Label(frame, text="Components coef", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
        label.grid(row=0, column=i, pady=10, sticky="w")

        # FREESKATING has the following options
        # - short program
        # - long program
        if self.category.type == "FREESKATING":

            statusList = ('UNSTARTED', 'SHORT', 'LONG', 'END')
            
            # short program
            self.shortVar = IntVar()

            if self.category.short:
                self.shortVar.set(1)

            ck = Checkbutton(frame, text="Short program", variable=self.shortVar, anchor='w', pady=10)
            ck.grid(row=1, column=0, pady=10, sticky="nsew")

            entry = Entry(frame, font=("monospace", 10), borderwidth=1, relief='flat')
            entry.insert(0, self.category.short_components)
            entry.grid(row=1, column=1, pady=10, sticky="nsew")
            self.shortCompoEntry = entry

            # long program
            self.longVar = IntVar()

            if self.category.long:
                self.longVar.set(1)

            ck = Checkbutton(frame, text="Long program", variable=self.longVar, anchor='w', pady=10)
            ck.grid(row=2, column=0, pady=10, sticky="nsew")

            entry = Entry(frame, font=("monospace", 10), borderwidth=1, relief='flat')
            entry.insert(0, self.category.long_components)
            entry.grid(row=2, column=1, pady=10, sticky="nsew")
            self.longCompoEntry = entry

            # End FREESKATING config

        # SOLO DANCE has the following options
        # - compulsory 1
        # - compulsory 2
        # - style dance
        # - free dance
        elif self.category.type == "SOLO DANCE":

            patterns = ('Quickstep', 'Starlight', 'Harris Tango Solo', 'Harris Tango Couples', 'Tango Delanco', 'Midnight Blues', 'Fourteen Step', 'Rocker Foxtrot', 'Blues Pattern', 'Terenzi Pattern', 'Westminster Waltz', 'Viennese Waltz', 'Paso Doble Pattern', 'Argentine Tango Solo', 'Argentine Tango', 'Italian Foxtrot', 'Castel March', 'City Blues', 'Carlos Tango', 'Skaters March', 'La Vista Cha Cha', 'Canasta Tango', 'Denver Shuffle', 'Tudor Waltz', 'Easy Paso', 'Association Waltz', 'Killian', 'Shaken Samba', 'Tango Delancha', 'Tango Iceland', 'Loran Rumba', 'Golden Samba', 'Roller Samba Couples', 'Roller Samba Solo', 'Cha Cha Patin', 'Little Waltz Couples', 'Little Waltz Solo', 'Flirtation Waltz Solo', 'Federation Foxtrot Solo', 'Kent Tango Solo', 'Siesta Tango SandC', 'Swing Foxtrot Couple')
            statusList = ('UNSTARTED', 'COMPULSORY1', 'COMPULSORY2', 'STYLE_DANCE', 'FREE_DANCE', 'END')

            # Compulsory dance 1
            self.compulsory1Var = IntVar()

            if self.category.compulsory1:
                self.compulsory1Var.set(1)

            ck = Checkbutton(frame, text="Compulsory Dance 1", variable=self.compulsory1Var, anchor='w', pady=10)
            ck.grid(row=1, column=0, pady=10, sticky="nsew")

            self.compulsory1DanceVar = StringVar()
            self.compulsory1DanceVar.set(self.category.compulsory1_pattern)
            om = OptionMenu(frame, self.compulsory1DanceVar, *patterns)
            om.configure(anchor="w")
            om.grid(row=1, column=1, pady=10, sticky="nsew")

            # Compulsory dance 2
            self.compulsory2Var = IntVar()

            if self.category.compulsory2:
                self.compulsory2Var.set(1)

            ck = Checkbutton(frame, text="Compulsory Dance 2", variable=self.compulsory2Var, anchor='w', pady=10)
            ck.grid(row=2, column=0, pady=10, sticky="nsew")

            self.compulsory2DanceVar = StringVar()
            self.compulsory2DanceVar.set(self.category.compulsory2_pattern)
            om = OptionMenu(frame, self.compulsory2DanceVar, *patterns)
            om.configure(anchor="w")
            om.grid(row=2, column=1, pady=10, sticky="nsew")

            # same compulsory components for all dances
            entry = Entry(frame, font=("monospace", 10), borderwidth=1, relief='flat')
            entry.insert(0, self.category.compulsory_components)
            entry.grid(row=1, column=2, rowspan=2, pady=10, sticky="nsew")
            self.compulsoryCompoEntry = entry

            # style dance
            self.style_danceVar = IntVar()

            if self.category.style_dance:
                self.style_danceVar.set(1)

            ck = Checkbutton(frame, text="Style dance", variable=self.style_danceVar, anchor='w', pady=10)
            ck.grid(row=3, column=0, pady=10, sticky="nsew")

            self.style_dancePatternVar = StringVar()
            self.style_dancePatternVar.set(self.category.style_dance_pattern)
            om = OptionMenu(frame, self.style_dancePatternVar, *patterns)
            om.configure(anchor="w")
            om.grid(row=3, column=1, pady=10, sticky="nsew")

            entry = Entry(frame, font=("monospace", 10), borderwidth=1, relief='flat')
            entry.insert(0, self.category.style_dance_components)
            entry.grid(row=3, column=2, pady=10, sticky="nsew")
            self.style_danceCompoEntry = entry

            # free dance
            self.free_danceVar = IntVar()

            if self.category.free_dance:
                self.free_danceVar.set(1)

            ck = Checkbutton(frame, text="Free dance", variable=self.free_danceVar, anchor='w', pady=10)
            ck.grid(row=4, column=0, pady=10, columnspan=2, sticky="nsew")

            entry = Entry(frame, font=("monospace", 10), borderwidth=1, relief='flat')
            entry.insert(0, self.category.free_dance_components)
            entry.grid(row=4, column=2, pady=10, sticky="nsew")
            self.free_danceCompoEntry = entry

            # End SOLO DANCE config

        frame.pack(fill=X, pady=10, padx=10)

        frame = Frame(self.frame, bg="#0a1526")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        label = Label(frame, text="Status", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
        label.grid(row=0, column=0, pady=10, sticky="w")

        self.statusVar = StringVar()
        self.statusVar.set(self.category.status)

        om = OptionMenu(frame, self.statusVar, *statusList)
        om.configure(anchor="w")
        om.grid(row=0, column=1, pady=10, sticky="nsew")

        frame.pack(fill=X, pady=10, padx=10)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.frame.grid(row=0, column=0, sticky="nesw")
    # End of config()


    # 
    # record()
    # Record opened category configuration
    def record(self):

        # 
        # Case FREESKATING
        if self.category.type == "FREESKATING":
            self.category.short = float(self.shortVar.get())
            self.category.long = float(self.longVar.get())
            self.category.short_components = float(self.shortCompoEntry.get())
            self.category.long_components = float(self.longCompoEntry.get())
            # end of case FREESKATING

        # Case SOLO DANCE
        elif self.category.type == "SOLO DANCE":
            self.category.compulsory1 = float(self.compulsory1Var.get())
            self.category.compulsory2 = float(self.compulsory2Var.get())
            self.category.style_dance = float(self.style_danceVar.get())
            self.category.free_dance = float(self.free_danceVar.get())
            self.category.compulsory_components = float(self.compulsoryCompoEntry.get())
            self.category.style_dance_components = float(self.style_danceCompoEntry.get())
            self.category.free_dance_components = float(self.free_danceCompoEntry.get())
            self.category.compulsory1_pattern = self.compulsory1DanceVar.get()
            self.category.compulsory2_pattern = self.compulsory2DanceVar.get()
            self.category.style_dance_pattern = self.style_dancePatternVar.get()
            # end of case SOLO DANCE

        self.category.status = self.statusVar.get()

        # Check if something is started in this category.
        # If nothing is started, category status is set to unstarted

        conn = tools.getDb()
        c = conn.cursor()
        c.row_factory = tools.dict_factory
        c.execute("SELECT COUNT(*) AS `num` FROM `skaters` WHERE `category` = ? AND `status` != 'unstarted'", (self.category.id,))
        res = c.fetchone()

        # unstarted
        if not res['num']:
            self.category.status = 'UNSTARTED'

        # End of status check

        self.category.record()

        self.list()
    # End of record()