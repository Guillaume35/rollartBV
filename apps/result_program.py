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

from apps.box_element import *

from motor.category import *

#
# ResultProgramApp(program = Program, parent = Object) Class
#
# This application open a window with all the program details, box per box, element per element.

class ResultProgramApp:

    def __init__(self, program, parent = None):
        self.window = None
        self.program = program
        self.frame = None

    #
    # open_window()
    # Display the complete details for skater results in a new window.
    def open_window(self):

        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("Program result - "+self.program.skater+" ("+self.program.program_name+") - RollArt BV")
        self.window.geometry("1600x850")
        self.window.minsize(1280,720)
        self.window.config(background="#0a1526")

        self.frame = Frame(self.window, bg="#0a1526")

        # Title frame
        label = Label(self.frame, text="Program result - "+self.program.skater+" ("+self.program.program_name+")", font=("sans-serif", 14), fg="white", bg="#0a1526")
        label.pack(fill=X, pady=15)

        category = Category(self.program.category)

        label = Label(self.frame, text=category.name, font=("sans-serif", 12), fg="white", bg="#0a1526")
        label.pack(fill=X, pady=15)

        # We are listing all boxes and call box element in readonly mode for display
        boxes = self.program.getBoxes()

        for box in boxes:
            comp = BoxElement(box, self.frame, self)
            comp.wrapper('readonly')
        # End of boxes loop

        # Technical score
        frame = Frame(self.frame, bg="#0a1526")

        label = Label(frame, text='Technical elements', font=("sans-serif", 12, 'bold'), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=0, column=0, sticky="nsew", ipady=10)

        label = Label(frame, text=self.program.technical_score, font=("sans-serif", 12, 'bold'), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=0, column=1, sticky="nsew", ipady=10)

        Grid.columnconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 1, minsize=200)

        frame.pack(fill=X, pady=15)
        # End of technical score

        components = ['skating_skills', 'transitions', 'choreography', 'performance']

        programData = self.program.getAll()

        # Components table
        frame = Frame(self.frame, bg="#0a1526")

        i = 0

        for component in components:
            label = Label(frame, text=component, font=("sans-serif", 10), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
            label.grid(row=i, column=0, sticky="nsew", ipady=10)

            label = Label(frame, text=programData[component], font=("sans-serif", 10), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
            label.grid(row=i, column=1, sticky="nsew", ipady=10)

            i += 1

        label = Label(frame, text='Components coef', font=("sans-serif", 10, 'bold'), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=i, column=0, sticky="nsew", ipady=10)

        # Display component coef depending on the program (short or long)
        if self.program.program_name.upper() == 'SHORT':
            val = category.long_components
        else:
            val = category.short_components
        # End of check program type

        label = Label(frame, text=str(val), font=("sans-serif", 10, 'bold'), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=i, column=1, sticky="nsew", ipady=10)
        i += 1

        # Total components
        label = Label(frame, text='Components', font=("sans-serif", 12, 'bold'), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=i, column=0, sticky="nsew", ipady=10)

        label = Label(frame, text=self.program.components_score, font=("sans-serif", 12, 'bold'), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=i, column=1, sticky="nsew", ipady=10)

        Grid.columnconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 1, minsize=200)
        
        frame.pack(fill=X, pady=15)
        # End of components table

        # Final score table
        frame = Frame(self.frame, bg="#0a1526")

        label = Label(frame, text=str(self.program.fall)+ ' Fall', font=("sans-serif", 10), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=0, column=0, sticky="nsew", ipady=10)

        label = Label(frame, text="Penalty "+str(self.program.penalization), font=("sans-serif", 10), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=0, column=1, sticky="nsew", ipady=10)

        label = Label(frame, text="SCORE", font=("sans-serif", 13, "bold"), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=RIGHT, anchor="e", padx=10)
        label.grid(row=0, column=2, sticky="nsew", ipady=10)

        label = Label(frame, text=self.program.score, font=("sans-serif", 13, "bold"), fg="white", bg="#0a1526", borderwidth=1, relief="groove", justify=LEFT, anchor="w", padx=10)
        label.grid(row=0, column=3, sticky="nsew", ipady=10)

        Grid.columnconfigure(frame, 2, weight=1)
        Grid.columnconfigure(frame, 3, minsize=200)

        frame.pack(fill=X, pady=15)
        # End of final score table

        self.frame.pack(fill=X)

        self.window.mainloop()
    # End of open_window()