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

from functools import partial
from tkinter import *

import tools

#
# PatternElement(element = ProgramElement, root = Frame, parent = BoxElement) Class
#
# Add a compulsory pattern section to a program with 2 modes : display or form. Form is for 
# the recording of the technical specialist information. Display is a readonly mode.
class PatternElement():

    def __init__(self, element, root, comp):
        self.root = root
        self.parent = comp
        self.element = element
        self.frame = None
        self.bas = None
        self.btnsBas = []

    def setBas(self, bas):

        for btn in self.btnsBas:
            if btn['text'] == bas:
                btn.configure(bg="cyan2", fg="black")
                btn.configure(activebackground="cyan2")

            else:

                if btn['text'] == 'Nlev':
                    btn.configure(bg="red", fg="white")
                else:
                    btn.configure(bg="#dfe7e8")
                
                btn.configure(activebackground="#dfe7e8")

        self.bas = bas
        self.check()

    def check(self):

        if (self.bas):
            self.element.code = self.bas
            self.element.read()
            self.element.calculate()
            self.element.record()

            self.display()

            self.parent.check()

    def form(self):

        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526")

        # Base value
        btns = ['Nlev']

        patterns = tools.compulsoryPatterns()

        if self.parent.program.program_name.upper() == 'STYLE_DANCE':
            pat = self.parent.category.style_dance_pattern
        elif self.parent.program.program_name.upper() == 'COMPULSORY1':
            pat = self.parent.category.compulsory1_pattern
        else:
            pat = self.parent.category.compulsory2_pattern

        pattern = patterns[pat]
        sec = self.parent.box.type.replace('PatternSection', '')

        if sec == 'Pattern':
            sec = '1'

        # Level can be Base (B), 1, 2, 3, 4
        # We use this label pattern : DANCECODE$L& where $ is the section number and & is the level code
        for lv in ['B', '1', '2', '3', '4']:
            label = pattern[1].replace('&', lv)
            label = label.replace('$', sec)
            btns.append(label)

        label = Label(self.frame, text=pat+' (Section '+sec+')', font=("sans-serif", 12, 'bold'), bg="#0a1526", fg="white")
        label.pack(pady=5)
        
        frame_step = Frame(self.frame, bg="#0a1526")

        i = 0

        for btnLabel in btns:
            self.btnsBas.append(Button(frame_step, text=btnLabel, font=("sans-serif", 11)))

            if btnLabel == 'Nlev':
                self.btnsBas[i].config(bg="red", fg="white")

            else:
                self.btnsBas[i].config(bg="#dfe7e8")

            self.btnsBas[i].config(command=lambda val=btnLabel: self.setBas(val))
            self.btnsBas[i].grid(row=1, column=i, sticky="nsew", ipadx=8, ipady=8)

            Grid.columnconfigure(frame_step, i, weight=1)

            i += 1

        frame_step.pack()

        self.frame.pack()

    def display(self):
        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526")

        label = Label(self.frame, text=self.element.code+' ('+self.element.label+')', font=("sans-serif", 12), bg="#0a1526", fg="white", justify=LEFT)
        label.pack(side=LEFT)

        self.frame.pack()