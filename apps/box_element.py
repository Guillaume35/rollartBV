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

import urllib.request
import urllib.parse

from apps.jump_element import *
from apps.choreo_element import *
from apps.spin_element import *
from apps.step_element import *

from motor.program import *
from motor.program_element import *
from motor.program_box import *

#
# BoxElement(box = ProgramBox, root = Frame, parent = Object) Class
#
# Add a box to a program with 2 modes : display or form. Form is for the recording of 
# the technical specialist information. display is for the recording of judge information.
# Display can be readonly so it is used for the result
class BoxElement():
    def __init__(self, box, root, parent):
        self.root = root
        self.parent = parent
        self.box = box
        self.frame = None
        self.frame_content = None
        self.lastElement = False
        self.btns = []
        self.mode = 'display'
        self.btnEdit = None
        self.btnDel = None
        self.readonly = False

    # 
    # wrapper(mode = String)
    # 4 possible modes : auto (decide to open form mode or display mode), form, display and readonly
    def wrapper(self, mode='auto'):

        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526", borderwidth=1, relief="groove")

        if mode == 'readonly':
            self.readonly = True

        Grid.rowconfigure(self.frame, self.box.order-1, weight=1)

        col = 0

        label = Label(self.frame, text="#"+str(self.box.order), font=("sans-serif", 14), bg="#bd3800", fg="white", padx=10, width=3)
        label.grid(row=self.box.order-1, column=col, sticky="nsew")

        col += 1

        if mode != 'readonly':
            self.btnEdit = Button(self.frame, text="Edit", font=("sans-serif", 11), bg="#dfe7e8", command=self.toggleMode)
            self.btnEdit.grid(row=self.box.order-1, column=col, sticky="nsew")

            col += 1

        Grid.columnconfigure(self.frame, col, weight=1)

        elements = self.box.getElements()

        if (self.box.id and len(elements) and mode != 'form') or mode == 'display' or mode == 'readonly':
            self.display()

        else:
            self.lastElement = True

            if not self.box.id:
                self.box.record()
            
            self.form()

        self.frame.pack(fill=X)

    def form(self):

        self.mode = 'form'

        self.btns = []

        if self.frame_content:
            self.frame_content.destroy()

        self.frame_content = Frame(self.frame, bg="#0a1526")

        frame_types = Frame(self.frame_content, bg="#0a1526")

        frame_element = Frame(self.frame_content, bg="#0a1526")

        Grid.rowconfigure(frame_types, 0, weight=1)

        # list elements types
        btnLabels = ['SoloJump', 'ComboJump', 'SoloSpin', 'ComboSpin', 'Step', 'Choreo']
        i = 0

        for btnLabel in btnLabels:

            Grid.columnconfigure(frame_types, i, weight=1)

            action = partial(self.element_form, btnLabel, frame_element)

            self.btns.append(Button(frame_types, text=btnLabel, font=("sans-serif", 13), bg="#dfe7e8", command=action))
            self.btns[i].grid(row=0, column=i, sticky="nsew", ipadx=6, ipady=6)
            i += 1

        if self.box.type:
            self.element_form(self.box.type, frame_element)

        frame_types.pack(pady=10, fill=X)
        frame_element.pack(pady=10, fill=X)

        action = partial(self.check, True)

        if self.lastElement:
            label="Next element"
        else:
            label="Save"

        tools_frame = Frame(self.frame_content, bg="#0a1526")

        Grid.columnconfigure(tools_frame, 0, weight=1)

        btn = Button(tools_frame, text=label, font=("sans-serif", 14, "bold"), bg="green", fg="white", pady=8, command=action)
        btn.grid(row=0, column=0, pady=10, sticky="nsew")

        btn = Button(tools_frame, text="Empty", font=("sans-serif", 14), bg="DarkOrange2", fg="white", pady=8, command=self.empty)
        btn.grid(row=0, column=1, pady=10, sticky="nsew")

        if not self.lastElement:
            btn = Button(tools_frame, text="Remove", font=("sans-serif", 14), bg="red", fg="white", pady=8, command=self.remove)
            btn.grid(row=0, column=2, pady=10, sticky="nsew")

        tools_frame.pack(fill=X)

        self.btnEdit.configure(bg="yellow")

        self.frame_content.grid(row=self.box.order-1, column=2, sticky="nsew")

    def display(self):

        if self.readonly:
            self.mode = 'readonly'
        else:
            self.mode = 'display'

        if self.frame_content:
            self.frame_content.destroy()

        self.frame_content = Frame(self.frame, bg="#0a1526")

        elements = self.box.getElements()

        i = 0

        for element in elements:
            element_frame = Frame(self.frame_content, bg="#0a1526")

            col = 0

            label = Label(element_frame, text=element.type, font=("sans-serif", 12), bg="#0a1526", fg="white", justify=LEFT, anchor="e")
            label.grid(row=i, column=col, padx=10, sticky="w")

            col += 1

            # Add star and time bonus button in all mode except readonly
            if self.mode != 'readonly':
                action = partial(self.star, element)

                btn = Button(element_frame, text="*", font=("sans-serif", 11), command=action)

                if element.star:
                    btn.configure(bg='yellow', fg='red')
                btn.grid(row=i, column=col, sticky="nsew")

                col += 1

                action = partial(self.time, element)

                btn = Button(element_frame, text="T", font=("sans-serif", 11), command=action)

                if element.time:
                    btn.configure(bg='yellow', fg='red')
                btn.grid(row=i, column=col, sticky="nsew")

                col += 1

            # Add label for star and time for readonly mode
            else:
                text = ''
                if element.star:
                    text = '*'
                
                label = Label(element_frame, text=text, font=("sans-serif", 12, "bold"), bg="#0a1526", fg="red")
                label.grid(row=i, column=col, padx=10)

                col += 1

                text = ''
                if element.time:
                    text = 'T'
                
                label = Label(element_frame, text=text, font=("sans-serif", 12, "bold"), bg="#0a1526", fg="white")
                label.grid(row=i, column=col, padx=10)

                col += 1
            # End of mode check for star and time button

            base_code = ''
            if element.value_label.lower() != 'base':
                base_code = element.value_label

            if element.bonus != '':
                base_code += '('+element.bonus+')'

            label = Label(element_frame, text=element.code+base_code, font=("sans-serif", 12), bg="#0a1526", fg="white", justify=LEFT, anchor="e")
            label.grid(row=i, column=col, sticky="w", padx=10)

            col += 1

            # Show QOE buttons if mode is not readonly
            if self.mode != 'readonly':
                if not element.star and element.base_value > 0:

                    qoes = [-3, -2, -1, 0, 1, 2, 3]

                    for qoe in qoes:
                        label = '+'+str(qoe) if qoe > 0 else str(qoe)
                        
                        if (int(qoe) == int(element.qoe)):
                            if qoe > 0:
                                color = "PaleGreen1"

                            elif qoe < 0:
                                color = "salmon"

                            else:
                                color = "DarkSlategray1"
                        
                        else:
                            color = "#dfe7e8"
                        
                        action = partial(self.setQoe, element, qoe)

                        btn = Button(element_frame, text=label, font=("sans-serif", 11), bg=color, command=action)
                        btn.grid(row=i, column=col, sticky="nsew")
                        col += 1
                
                else:
                    col += 7
            
            # Mode is readonly, we only display applied QOE
            else:
                color = 'white'
                if not element.star and element.base_value > 0:
                    label = str(element.qoe)
                    if int(element.qoe) > 0:
                        label = '+'+label
                        color = "PaleGreen1"
                    elif int(element.qoe) < 0:
                        color = "salmon"
                    else:
                        color = "DarkSlategray1"
                else:
                    label = ''
                
                label = Label(element_frame, text=label, font=("sans-serif", 12), bg="#0a1526", fg=color)
                label.grid(row=i, column=col, sticky="w", padx=10)
                col += 1
            # End of check readonly mode

            label = Label(element_frame, text=element.stared_value, font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.grid(row=i, column=col, sticky="w", padx=10)

            col += 1

            # cols configuration in all mode except readonly
            if self.mode != 'readonly':
                Grid.columnconfigure(element_frame, 0, weight=1)
                Grid.columnconfigure(element_frame, 1)
                Grid.columnconfigure(element_frame, 2)
                Grid.columnconfigure(element_frame, 3, minsize=300)

                j = 0

                while j < 7:
                    Grid.columnconfigure(element_frame, 4+j, minsize=90)
                    j += 1

                Grid.columnconfigure(element_frame, 11, minsize=150)

            # cols configuration in readonly mode
            else:
                Grid.columnconfigure(element_frame, 0)
                Grid.columnconfigure(element_frame, 1, minsize=50)
                Grid.columnconfigure(element_frame, 2, minsize=50)
                Grid.columnconfigure(element_frame, 3, minsize=300)
                Grid.columnconfigure(element_frame, 4, minsize=90)
                Grid.columnconfigure(element_frame, 5, minsize=200)
            # End of mode check


            element_frame.pack(fill=X)

            i += 1

        if self.mode != 'readonly':
            self.btnEdit.configure(bg="#dfe7e8")
        self.frame_content.grid(row=self.box.order-1, column=2, sticky="nsew")

    def toggleMode(self):

        elements = self.box.getElements()

        if self.mode == 'form' and len(elements) and not self.lastElement:
            self.check()
            self.display()
        
        elif self.mode == 'display':
            self.form()

    def empty(self):
        self.box.empty()
        self.form()

    def remove(self):
        program_id = self.box.program
        self.box.delete()
        program = Program(program_id)
        self.parent.open_program(program)

    def check(self, force=False):
        
        elements = self.box.getElements()

        if len(elements) and (self.box.type == 'SoloJump' or self.box.type == 'SoloSpin' or self.box.type == 'Choreo' or self.box.type == 'Step' or force):

            if len(elements) > 1 and (self.box.type == 'SoloJump' or self.box.type == 'SoloSpin' or self.box.type == 'Choreo' or self.box.type == 'Step'):
                lastAdded = elements[-1]
                self.box.empty()
                lastAdded.record()

            self.box.record()

            self.display()

            self.parent.program_score()

            if self.lastElement:
                comp = BoxElement(ProgramBox({
                    'program': self.box.program,
                    'type': None
                }), self.root, self.parent)
                comp.wrapper()

                self.parent.boxes.append(comp)

                self.lastElement = False

            lastAdded = elements[-1]
            if lastAdded:

                label = ''
                if lastAdded.value_label.upper() != 'BASE':
                    label = lastAdded.value_label
                
                code = urllib.parse.quote_plus(lastAdded.code+label)
                self.parent.program.calculate()

                url = 'https://www.raiv.fr/wintercup2020/data.php?liveScoreEl='+code+'&liveScoreVal='+str(lastAdded.base_value)+'&liveScoreSk='+str(self.parent.program.total_score)
                urllib.request.urlopen(url)

    def star(self, element):
        if element.star:
            element.star = 0
        else:
            element.star = 1
        
        element.calculate()
        element.record()
        
        self.display()
        self.parent.program_score()

    def time(self, element):
        if element.time:
            element.time = 0
        else:
            element.time = 1
        
        element.calculate()
        element.record()
        
        self.display()
        self.parent.program_score()

    def setQoe(self, element, qoe):
        element.qoe = qoe
        element.calculate()
        element.record()
        self.display()
        self.parent.program_score()

    def element_form(self, typeCode, frame):

        # Check button
        for btn in self.btns:
            if btn['text'] == typeCode:
                btn.configure(bg="yellow")
                btn.configure(activebackground="yellow")

            else:
                btn.configure(bg="#dfe7e8")
                btn.configure(activebackground="#dfe7e8")

        ws = frame.winfo_children()

        for w in ws:
            w.destroy()

        # Empty the box if type has change
        if self.box.type != typeCode:
            self.box.empty()
        
        self.box.type = typeCode

        elements = self.box.getElements()
        elements.append(ProgramElement({
            'box': self.box.id,
            'program': self.box.program,
            'type': self.box.type
        }))

        for element in elements:
            if (typeCode == 'SoloJump' or typeCode == 'ComboJump'):
                comp = JumpElement(element, frame, self)

            elif (typeCode == 'SoloSpin' or typeCode == 'ComboSpin'):
                comp = SpinElement(element, frame, self)

            elif (typeCode == 'Step'):
                comp = StepElement(element, frame, self)

            elif (typeCode == 'Choreo'):
                comp = ChoreoElement(element, frame, self)
                
            if element.id:
                comp.display()
            
            else:
                comp.form()