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

from motor.program_element import *

#
# JumpElement(element = ProgramElement, root = Frame, parent = BoxElement) Class
class JumpElement():

    """
    * Add a jump element to a program with 2 modes : display or form. Form is for 
    * the recording of the technical specialist information. Display is a readonly mode.
    * Jump can be SoloJump or ComboJump type
    """

    def __init__(self, element, root, parent):
        self.root = root
        self.parent = parent
        self.element = element
        self.frame = None
        self.rot = None
        self.jum = None
        self.bas = None
        self.btnsJum = []
        self.btnsRot = []
        self.btnsBas = []

    def setRot(self, rot):

        for btn in self.btnsRot:
            if btn['text'] == rot:
                btn.configure(bg="cyan2")
                btn.configure(activebackground="cyan2")

            else:
                btn.configure(bg="#dfe7e8")
                btn.configure(activebackground="#dfe7e8")

        self.rot = rot
        self.check()

    def setJum(self, jum):

        for btn in self.btnsJum:
            if btn['text'] == jum:
                btn.configure(bg="cyan2")
                btn.configure(activebackground="cyan2")

            else:
                btn.configure(bg="#dfe7e8")
                btn.configure(activebackground="#dfe7e8")

        self.jum = jum
        self.check()

    def setBas(self, bas):

        for btn in self.btnsBas:
            if btn['text'] == bas:
                btn.configure(bg="cyan2")
                btn.configure(activebackground="cyan2")

            else:
                btn.configure(bg="#dfe7e8")
                btn.configure(activebackground="#dfe7e8")

        self.bas = bas
        self.check()

    def check(self):

        if (self.rot == 'NJ' or (self.rot and self.jum and self.bas)):
            prev_id = self.element.id

            if self.rot == 'NJ':
                self.element.code = self.rot
                self.element.label = 'No Jump'
                self.element.base_value = 0

            elif self.rot and self.jum and self.bas:
                code = str(self.rot) + self.jum
                self.element.code = code
                self.element.value_label = self.bas
                self.element.read()
            
            self.element.calculate()
            self.element.record()

            self.display()

            if not prev_id and self.element.type == 'ComboJump':
                comp = JumpElement(ProgramElement({
                    'box': self.element.box,
                    'program': self.element.program,
                    'type': self.element.type
                }), self.root, self.parent)
                comp.form()

            self.parent.check()

    def form(self):

        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526")

        # Number of rotation
        btns = ['NJ', 1, 2, 3, 4]

        frame_rotation = Frame(self.frame, bg="#0a1526")

        #Grid.rowconfigure(frame_rotation, 0, weight=1)

        i = 0

        for btnLabel in btns:
            self.btnsRot.append(Button(frame_rotation, text=btnLabel, font=("sans-serif", 11), bg="#dfe7e8"))
            self.btnsRot[i].config(command=lambda val=btnLabel: self.setRot(val))
            self.btnsRot[i].grid(row=0, column=i, sticky="nsew", ipadx=8, ipady=8)

            Grid.columnconfigure(frame_rotation, i, weight=1)

            i += 1

        frame_rotation.pack()


        # Jump
        btns = ['W', 'T', 'S', 'F', 'Lz', 'LzNE', 'Lo', 'Th', 'A']
        
        frame_jump = Frame(self.frame, bg="#0a1526")

        #Grid.rowconfigure(frame_jump, 1, weight=1)

        i = 0

        for btnLabel in btns:
            self.btnsJum.append(Button(frame_jump, text=btnLabel, font=("sans-serif", 11), bg="#dfe7e8"))
            self.btnsJum[i].config(command=lambda val=btnLabel: self.setJum(val))
            self.btnsJum[i].grid(row=1, column=i, sticky="nsew", ipadx=8, ipady=8)

            Grid.columnconfigure(frame_jump, i, weight=1)

            i += 1

        frame_jump.pack()


        # Base value
        btns = ['Base', '<', '<<', '<<<']
        
        frame_base = Frame(self.frame, bg="#0a1526")

        i = 0

        #Grid.rowconfigure(frame_base, 2, weight=1)

        for btnLabel in btns:
            self.btnsBas.append(Button(frame_base, text=btnLabel, font=("sans-serif", 11), bg="#dfe7e8"))
            self.btnsBas[i].config(command=lambda val=btnLabel: self.setBas(val))
            self.btnsBas[i].grid(row=2, column=i, sticky="nsew", ipadx=8, ipady=8)

            Grid.columnconfigure(frame_base, i, weight=1)

            i += 1

        frame_base.pack()

        self.frame.pack()

    def display(self):
        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526")

        base_code = ''
        if self.element.value_label.lower() != 'base':
            base_code = self.element.value_label

        label = Label(self.frame, text=self.element.code+base_code+' ('+self.element.label+')', font=("sans-serif", 12), bg="#0a1526", fg="white", justify=LEFT)
        label.pack(side=LEFT)

        self.frame.pack()