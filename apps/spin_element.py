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
# SpinElement(element = ProgramElement, root = Frame, parent = BoxElement) Class
#
# Add a spin element to a program with 2 modes : display or form. Form is for 
# the recording of the technical specialist information. Display is a readonly mode.
# Spin can be SoloSpin or ComboSpin type.
class SpinElement():

    def __init__(self, element, root, comp):
        self.root = root
        self.parent = comp
        self.element = element
        self.frame = None
        self.spi = None
        self.bon = []
        self.btnsSpi = []
        self.btnsBon = []

    def setSpi(self, spi):

        for btn in self.btnsSpi:
            if btn['text'] == spi:
                btn.configure(bg="cyan2", fg="black")
                btn.configure(activebackground="cyan2")

            else:

                if btn['text'] == 'NC':
                    btn.configure(bg="red", fg="white")
                else:
                    btn.configure(bg="#dfe7e8")
                
                btn.configure(activebackground="#dfe7e8")

        self.spi = spi
        self.check()

    def setBon(self, bon):

        if bon in self.bon:
            self.bon.remove(bon)

        else:
            self.bon.append(bon)

        for btn in self.btnsBon:
            if btn['text'] in self.bon:
                btn.configure(bg="cyan2")
                btn.configure(activebackground="cyan2")

            else:
                btn.configure(bg="#dfe7e8")
                btn.configure(activebackground="#dfe7e8")

        self.check()

    def check(self, force=False):

        if (self.spi == 'NC' or (self.spi and force)):
            prev_id = self.element.id

            if self.spi == 'NC':
                self.element.code = 'NS'
                self.element.label = 'No Spin'
                self.element.base_value = 0

            else:
                self.element.code = self.spi
                self.element.read()
                self.element.bonus = ','.join(self.bon)
            
            self.element.calculate()
            self.element.record()

            self.display()

            if not prev_id and self.element.type == 'ComboSpin':
                comp = SpinElement(ProgramElement({
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

        # Spin
        btns = ['NC', 'U', 'S', 'C', 'Br', 'H', 'In']
        
        frame_spin = Frame(self.frame, bg="#0a1526")

        i = 0

        for btnLabel in btns:
            self.btnsSpi.append(Button(frame_spin, text=btnLabel, font=("sans-serif", 11)))

            if btnLabel == 'NC':
                self.btnsSpi[i].config(bg="red", fg="white")

            else:
                self.btnsSpi[i].config(bg="#dfe7e8")

            self.btnsSpi[i].config(command=lambda val=btnLabel: self.setSpi(val))
            self.btnsSpi[i].grid(row=1, column=i, sticky="nsew", ipadx=8, ipady=8)

            Grid.columnconfigure(frame_spin, i, weight=1)

            i += 1

        frame_spin.pack()


        # Bonus
        btns = ['Fw', 'Sw', 'Bh', 'Ly', 'Biel', 'T', 'LO', 'Bry', 'DE', '6R', '4R', 'H']

        if (self.element.type == 'ComboSpin'):
            btns.append('SBC')
            btns.append('DCH')
            btns.append('BD')
        
        frame_bonus = Frame(self.frame, bg="#0a1526")

        i = 0

        for btnLabel in btns:
            self.btnsBon.append(Button(frame_bonus, text=btnLabel, font=("sans-serif", 11), bg="#dfe7e8"))
            self.btnsBon[i].config(command=lambda val=btnLabel: self.setBon(val))
            self.btnsBon[i].grid(row=2, column=i, sticky="nsew", ipadx=8, ipady=8)

            Grid.columnconfigure(frame_bonus, i, weight=1)

            i += 1

        frame_bonus.pack()

        btn = Button(self.frame, text="Confirmed", font=("sans-serif", 11), bg="green", fg="white")
        btn.config(command=lambda val=True: self.check(val))
        btn.pack(fill=X, ipadx=8, ipady=8)

        self.frame.pack()

    def display(self):
        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526")

        label = Label(self.frame, text=self.element.code+' '+self.element.bonus+' ('+self.element.label+')', font=("sans-serif", 12), bg="#0a1526", fg="white", justify=LEFT)
        label.pack(side=LEFT)

        self.frame.pack()
