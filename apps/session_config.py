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

from tkinter import *
from tkinter import messagebox

import urllib.request
from functools import partial

#
# SessionConfigApp(parent = RollartApp) Class
class SessionConfigApp():

    """
    * Application for session configuration.
    """

    def __init__(self, parent):
        self.window = None
        self.frame = None
        self.parent = parent
        self.session = parent.session
        self.onlineVar = None

        self.nameEntry = None
        self.dateEntry = None
        self.displayUrlEntry = None


    #
    # record()
    def record(self):

        # Check server
        er = 0
        if self.onlineVar.get():
            try:
                status_code = urllib.request.urlopen(self.displayUrlEntry.get()).getcode()
            except:
                er += 1
                messagebox.showwarning(title="Invalid server", message="Error while opening server. Check the server configuration or your internet connection. Disable online checkbox to ignore server.", parent=self.window)
            
            if not er:
                # Invalid server
                if status_code != 200:
                    er += 1
                    messagebox.showwarning(title="Invalid server", message="Server is invalid (CODE : "+status_code+"). Disable online checkbox or valid a correct server URL.", parent=self.window)

        if not er:
            self.session.name = self.nameEntry.get()
            self.session.date = self.dateEntry.get()
            self.session.display_url = self.displayUrlEntry.get()
            self.session.online = int(self.onlineVar.get())
            self.session.record()

            self.parent.sessionLabel.configure(text=self.session.name)

            self.window.destroy()
    # End record()
    

    # 
    # open_window()
    def open_window(self):
        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("Configure session - "+self.session.name+" - RollArt Unchained")
        self.window.geometry("800x300")
        self.window.minsize(800,300)
        self.window.config(background="#0a1526")

        self.frame = Frame(self.window, bg="#0a1526")

        # Title frame

        title_frame = Frame(self.frame, bg="#bd3800")

        btn = Button(title_frame, text="Close", font=("sans-serif", 12), command=self.window.destroy)
        btn.grid(row=0, column=0, sticky="nsew")

        label = Label(title_frame, text="Configure session - "+self.session.name, font=("sans-serif", 14), fg="white", bg="#bd3800")
        label.grid(row=0, column=1, sticky="nsw", padx="10")

        btn = Button(title_frame, text="Save", font=("sans-serif", 12), bg="green", fg="white", command=self.record)
        btn.grid(row=0, column=2, sticky="nsew")

        Grid.columnconfigure(title_frame, 1, weight=1)

        title_frame.pack(fill=X)

        # General informations
        frame = Frame(self.frame, bg="#0a1526")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        label = Label(frame, text="Name", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
        label.grid(row=0, column=0, padx=10, sticky="w")

        entry = Entry(frame, font=("sans-serif", 10), borderwidth=1, relief='flat')
        entry.insert(0, self.session.name)
        entry.grid(row=1, column=0, padx=10, sticky="nsew")
        self.nameEntry = entry

        label = Label(frame, text="Date", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
        label.grid(row=0, column=1, padx=10, sticky="w")

        entry = Entry(frame, font=("sans-serif", 10), borderwidth=1, relief='flat')
        entry.insert(0, self.session.date)
        entry.grid(row=1, column=1, padx=10, sticky="nsew")
        self.dateEntry = entry

        frame.pack(fill=X, pady=10)

        # Display and output system
        frame = Frame(self.frame, bg="#0a1526")
        frame.grid_columnconfigure(0, weight=1)

        label = Label(frame, text="Display URL", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
        label.grid(row=0, column=0, padx=10, sticky="w")

        entry = Entry(frame, font=("sans-serif", 10), borderwidth=1, relief='flat')
        entry.insert(0, str(self.session.display_url))
        entry.grid(row=1, column=0, padx=10, sticky="nsew")
        self.displayUrlEntry = entry

        frame.pack(fill=X, pady=10)

        self.onlineVar = IntVar()

        if self.session.online:
           self.onlineVar.set(self.session.online)

        ck = Checkbutton(self.frame, text="Host session online (need internet connection)", variable=self.onlineVar)
        ck.configure(command=partial(self.toggleCk, self.onlineVar, ck))
        if int(self.onlineVar.get()):
            ck.select()
        else:
            ck.deselect()
        ck.pack(pady=10, padx=10)

        self.frame.pack(fill=X)

        self.window.mainloop()
    # End of open_window()


    #
    # toggleCk(var = tkinter.Var, ck = Checkbutton)
    def toggleCk(self, var, ck):

        if var.get():
            ck.deselect()
            var.set(0)
        else:
            ck.select()
            var.set(1)
    # End of toggleCk()