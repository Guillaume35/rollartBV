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
from tkinter import messagebox
import tools
import numpy
from functools import partial

class ComponentApp:

    def __init__(self, component, parent):
        self.parent = parent
        self.window = None
        self.entry = None
        self.component = component
        self.btnsUnit = []
        self.btnsDeci = []
        self.unit = 0
        self.deci_frame = None
        self.closed = False

        comData = self.parent.program.getAll()
        part = str(comData[self.component]).split('.')

        self.unit = int(part[0])

    def confirm(self):
        val = float(self.entry.get())

        if val <= 0:
            self.parent.program.penalization = val
            self.parent.program.record()
            self.parent.program_score()
            self.close_window()

        else:
            messagebox.showwarning(title="Penalty alert", message="Only <= 0 value accepted", parent=self.window)

    def close_window(self):
        self.closed = True
        self.window.destroy()

    def open_window(self):

        # Create main window
        self.window = Tk()

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # Customizing window
        self.window.title("Component "+self.component+" - RollArt BV")
        self.window.geometry("800x300")
        self.window.minsize(480,360)
        self.window.config(background="#0a1526")

        comData = self.parent.program.getAll()
        part = str(comData[self.component]).split('.')

        frame = Frame(self.window, bg="")

        label = Label(frame, text="Component "+self.component, font=("sans-serif", 14), bg="#0a1526", fg="white")
        label.pack(fill=X, pady=10)

        row = Frame(frame, bg="")

        for i in range(0,11):

            action = partial(self.selectUnit, i)

            self.btnsUnit.append(Button(row, text=i, font=('sans-serif', 14), padx=10, pady=10, command=action))

            if i == int(part[0]):
                self.btnsUnit[i].configure(bg="cyan2")
                self.btnsUnit[i].configure(activebackground="cyan2")

            else:
                self.btnsUnit[i].configure(bg="#dfe7e8")
                self.btnsUnit[i].configure(activebackground="#dfe7e8")

            self.btnsUnit[i].grid(row=0, column=i, sticky="nsew", pady=10)

            Grid.columnconfigure(row, i, weight=1)

        row.pack(fill=X)

        self.deci_frame = Frame(frame, bg="")

        self.deciForm()

        self.deci_frame.pack(fill=X)

        frame.pack(fill=X)

        # display window
        self.window.mainloop()

    def selectUnit(self, val):

        if val != self.unit:

            for btn in self.btnsUnit:
                if btn['text'] == val:
                    btn.configure(bg="cyan2")
                    btn.configure(activebackground="cyan2")

                else:
                    btn.configure(bg="#dfe7e8")
                    btn.configure(activebackground="#dfe7e8")

            self.unit = val

            self.deciForm()

    def selectVal(self, val):

        if val > 0 and val <= 10:

            if self.component == 'skating_skills':
                self.parent.program.skating_skills = val
            elif self.component == 'transitions':
                self.parent.program.transitions = val
            elif self.component == 'choreography':
                self.parent.program.choreography = val
            elif self.component == 'performance':
                self.parent.program.performance = val

            self.parent.program.record()
            self.parent.program_component_value(self.component)
            self.parent.program_score()
            self.close_window()

    def deciForm(self):

        for widget in self.deci_frame.winfo_children():
            widget.destroy()

        j = 0

        comData = self.parent.program.getAll()

        for i in numpy.arange(self.unit, self.unit+1, 0.25):

            if i > 0 and i <= 10:

                action = partial(self.selectVal, i)

                btn = Button(self.deci_frame, text=i, font=('sans-serif', 14), padx=10, pady=10, command=action)

                if i == comData[self.component]:
                    btn.configure(bg="cyan2")
                    btn.configure(activebackground="cyan2")

                else:
                    btn.configure(bg="#dfe7e8")
                    btn.configure(activebackground="#dfe7e8")

                btn.grid(row=0, column=j, sticky="nsew")

                Grid.columnconfigure(self.deci_frame, j, weight=1)

                j += 1
