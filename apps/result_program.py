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

#
# ResultProgramApp(program = Program, parent = Object) Class
#
# This application open a window with all the program details, box per box, element per element.

class ResultProgramApp:

    def __init__(self, program, parent = None):
        self.window = None
        self.program = program

    #
    # open_window()
    def open_window(self):

        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("Program result - "+program.skater+" ("+program.name+") - RollArt BV")
        self.window.geometry("1600x850")
        self.window.minsize(1280,720)
        self.window.config(background="#0a1526")

        self.window.mainloop()