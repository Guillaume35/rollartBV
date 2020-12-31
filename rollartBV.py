from tkinter import *
import elements_database
import types_database
import sessions_database
from functools import partial
from motor.program import *
from motor.session import *
from motor.category import *
from motor.element import *
from motor.element_type import *
from motor.program_element import *
import tools

class RollartApp:

    def __init__(self):
        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("RollArt BV")
        self.window.geometry("500x720")
        self.window.minsize(480,360)
        self.window.config(background="#0a1526")

        # global variables
        self.frame = None
        self.skater_entry = None
        self.program_entry = None
        self.error_label = None
        self.element_i = 1
        self.boxes_frame = None
        self.elements_form = None
        self.score_frame = None
        self.program = None


    #start program
    def start(self):

        skater = self.skater_entry.get()
        program_name = self.program_entry.get()

        if skater == '' or program_name == '':
            self.error_label.config(text="You must set Skater and Program information")
            self.error_label.pack(pady=5, padx=5)

        else:
            program = Program({
                'skater': skater, 
                'program_name': program_name
            })

            program.record()

            self.program = program

            self.open_program(program)


    # Display home
    def home(self):

        # Destroy frame if already inited
        if (self.frame):
            self.frame.pack_forget()
            self.frame.destroy()

        # create frame
        self.frame = Frame(self.window, bg="#0a1526")
        title_frame = Frame(self.frame, bg="#0a1526")
        menu_frame = Frame(self.frame, bg="#0a1526")
        session_frame = Frame(self.frame, bg="#0a1526")

        # create elements

        # title
        label_title = Label(title_frame, text="RollArt BV", font=("sans-serif", 24), bg="#0a1526", fg="white")
        label_title.pack()

        label_subtitle = Label(title_frame, text="Calculate your program base value in real time !", font=("sans-serif", 14), bg="#0a1526", fg="white")
        label_subtitle.pack()

        # check current session
        currentSession = Session.getOpened()

        # current session exists
        if currentSession:

            label_session = Label(session_frame, text=currentSession.name, font=("sans-serif", 12), bg="#0a1526", fg="white")
            label_session.pack(pady=10)

            sessionAction = partial(sessions_database.close_session, currentSession, self)

            sessions_db_btn = Button(session_frame, text="Close session", font=("sans-serif", 12), bg="#cf362b", fg="white", command=sessionAction)
            sessions_db_btn.pack(pady=5, fill=X)

        else:
            sessionAction = partial(sessions_database.open_window, self)

            # Session menu
            sessions_db_btn = Button(session_frame, text="Open session", font=("sans-serif", 12), bg="#dfe7e8", command=sessionAction)
            sessions_db_btn.pack(pady=5, fill=X)

        # menu
        error_frame = Frame(menu_frame, bg="red")
        self.error_label = Label(error_frame, text="", font=("sans-serif", 10), bg="red", fg="white", height=0)
        error_frame.pack()

        if not currentSession:
            # Skater informations
            form_frame = Frame(menu_frame, bg="#0a1526")
            skater_label = Label(form_frame, text="Skater", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
            skater_label.grid(row=0, column=0, sticky="nw")
            self.skater_entry = Entry(form_frame, font=('sans-serif', 10), borderwidth=1, relief='flat')
            self.skater_entry.grid(row=1, column=0, sticky="nesw", ipadx=5, ipady=5)

            program_label = Label(form_frame, text="Program", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
            program_label.grid(row=0, column=1, sticky="nw")
            self.program_entry = Entry(form_frame, font=('sans-serif', 10), borderwidth=1, relief='flat')
            self.program_entry.grid(row=1, column=1, sticky="nesw", ipadx=5, ipady=5)

            form_frame.pack(pady=5, expand=YES)

        else:
            # get next skater
            label_skater = Label(menu_frame, text="> Next skater ???", font=("sans-serif", 14, "bold"), bg="#0a1526", fg="white")
            label_skater.pack(pady=5)

        # Buttons
        start_btn = Button(menu_frame, text="Start", font=("sans-serif", 14, "bold"), bg="#bd3800", fg="white", pady=8, command=self.start)
        start_btn.pack(pady=10, fill=X)

        # Managing skaters list
        if currentSession:
            label = Label(menu_frame, text="Current session managment", font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.pack(pady=10)

            btn = Button(menu_frame, text="Categories", font=("sans-serif", 12), bg="#dfe7e8")
            btn.pack(pady=5, fill=X)

            btn = Button(menu_frame, text="Skaters", font=("sans-serif", 12), bg="#dfe7e8")
            btn.pack(pady=5, fill=X)


        label = Label(menu_frame, text="RollArt configuration", font=("sans-serif", 12), bg="#0a1526", fg="white")
        label.pack(pady=10)

        elements_db_btn = Button(menu_frame, text="Elements database", font=("sans-serif", 12), bg="#dfe7e8", command=elements_database.open_window)
        elements_db_btn.pack(pady=5, fill=X)

        types_db_btn = Button(menu_frame, text="Types database", font=("sans-serif", 12), bg="#dfe7e8", command=types_database.open_window)
        types_db_btn.pack(pady=5, fill=X)

        # add to window
        title_frame.pack(pady=15)
        session_frame.pack(pady=15, fill=X)
        menu_frame.pack(pady=15, fill=X)
        self.frame.pack(expand=YES)

    # program window
    def open_program(self, program):

        if self.frame:
            self.frame.destroy()

        #Grid.columnconfigure(window, 0, weight=1)
        #Grid.rowconfigure(window, 0, weight=1)

        # create frame
        self.frame = Frame(self.window, bg="#0a1526")
        self.boxes_frame = Frame(self.frame,  bg="#0a1526")

        #Grid.columnconfigure(frame, 0, weight=1)
        #Grid.rowconfigure(frame, 0, weight=1)

        title_frame = Frame(self.frame, bg="#bd3800")

        Grid.columnconfigure(title_frame, 0, weight=1)
        Grid.rowconfigure(title_frame, 0, weight=1)

        # title
        label_title = Label(title_frame, text="Record program", font=("sans-serif", 18), bg="#bd3800", fg="white", padx=10)
        label_title.grid(row=0, column=0, sticky="nsw")

        Grid.columnconfigure(title_frame, 1, weight=1)

        label_skater = Label(title_frame, text=program.skater+' ('+program.program_name+')', font=("sans-serif", 10), bg="#bd3800", fg="white", padx=10)
        label_skater.grid(row=0, column=1, sticky="nes")

        # add to window
        title_frame.pack(ipady=5, fill=X)

        boxes = program.getBoxes()

        createEmpty = True

        if len(boxes):
            lastCreated = boxes[-1]
            elements = lastCreated.getElements()

            if not len(elements):
                createEmpty = False
        
        if createEmpty:
            boxes.append(ProgramBox({
                'program': program.id
            }))

        i = 0

        for box in boxes:

            comp = BoxElement(box, self.boxes_frame, self)
            comp.wrapper()

            i += 1

        #self.program_element_form()
        self.boxes_frame.pack(fill=X)

        self.program_score()

        self.frame.pack(fill=X)

    # Refresh score program
    def program_score(self):

        if self.score_frame:
            self.score_frame.destroy()

        self.score_frame = Frame(self.frame,  bg="#0a1526")

        self.program.calculate()
        self.program.record()

        label = Label(self.score_frame, text="Technical Score", font=("sans-serif", 12), bg="#0a1526", fg="white", borderwidth=1, relief="groove", anchor="e", justify=RIGHT, padx=10)
        label.grid(row=0, column=0, sticky="nesw")
        label = Label(self.score_frame, text=self.program.technical_score, font=("sans-serif", 12), bg="#0a1526", fg="white", borderwidth=1, relief="groove", anchor="w", justify=LEFT, padx=10)
        label.grid(row=0, column=1, sticky="nesw")

        label = Label(self.score_frame, text="Components", font=("sans-serif", 12), bg="#0a1526", fg="white", borderwidth=1, anchor="e", relief="groove", padx=10)
        label.grid(row=1, column=0, sticky="nesw")
        label = Label(self.score_frame, text=self.program.components_score, font=("sans-serif", 12), bg="#0a1526", fg="white", borderwidth=1, anchor="w", relief="groove", padx=10)
        label.grid(row=1, column=1, sticky="nesw")

        label = Label(self.score_frame, text="Penalization", font=("sans-serif", 12), bg="#0a1526", fg="white", borderwidth=1, anchor="e", relief="groove", padx=10)
        label.grid(row=2, column=0, sticky="nesw")
        label = Label(self.score_frame, text=self.program.penalization, font=("sans-serif", 12), bg="#0a1526", fg="white", borderwidth=1, anchor="w", relief="groove", padx=10)
        label.grid(row=2, column=1, sticky="nesw")

        label = Label(self.score_frame, text="Score", font=("sans-serif", 14), bg="#0a1526", fg="white", borderwidth=1, anchor="e", relief="groove", padx=10)
        label.grid(row=3, column=0, sticky="nesw")
        label = Label(self.score_frame, text=self.program.score, font=("sans-serif", 14), bg="#0a1526", fg="white", borderwidth=1, anchor="w", relief="groove", padx=10)
        label.grid(row=3, column=1, sticky="nesw")

        Grid.columnconfigure(self.score_frame, 0, weight=1)
        Grid.columnconfigure(self.score_frame, 1, minsize=300)

        self.score_frame.pack(fill=X, pady=10)

            
# Add a box
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

    def wrapper(self, mode='auto'):

        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.root, bg="#0a1526", borderwidth=1, relief="groove")

        Grid.rowconfigure(self.frame, self.box.order-1, weight=1)

        label = Label(self.frame, text="#"+str(self.box.order), font=("sans-serif", 14), bg="#bd3800", fg="white", padx=10, width=3)
        label.grid(row=self.box.order-1, column=0, sticky="nsew")

        self.btnEdit = Button(self.frame, text="Edit", font=("sans-serif", 11), bg="#dfe7e8", command=self.toggleMode)
        self.btnEdit.grid(row=self.box.order-1, column=1, sticky="nsew")

        Grid.columnconfigure(self.frame, 2, weight=1)

        elements = self.box.getElements()

        if (self.box.id and len(elements) and mode != 'form') or mode == 'display':
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

        self.mode = 'display'

        if self.frame_content:
            self.frame_content.destroy()

        self.frame_content = Frame(self.frame, bg="#0a1526")

        elements = self.box.getElements()

        i = 0

        for element in elements:
            element_frame = Frame(self.frame_content, bg="#0a1526")

            label = Label(element_frame, text=element.type, font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.grid(row=i, column=0, sticky="w", padx=10)

            action = partial(self.star, element)

            btn = Button(element_frame, text="*", font=("sans-serif", 11), command=action)

            if element.star:
                btn.configure(bg='yellow', fg='red')
            btn.grid(row=i, column=1, sticky="nsew")

            btn = Button(element_frame, text="T", font=("sans-serif", 11))
            btn.grid(row=i, column=2, sticky="nsew")

            base_code = ''
            if element.value_label.lower() != 'base':
                base_code = element.value_label

            if element.bonus != '':
                base_code += '('+element.bonus+')'

            label = Label(element_frame, text=element.code+base_code, font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.grid(row=i, column=3, sticky="w", padx=10)

            if not element.star and element.base_value > 0:

                qoes = [-3, -2, -1, 0, 1, 2, 3]
                j = 1

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
                    btn.grid(row=i, column=3+j, sticky="nsew")
                    j += 1

            label = Label(element_frame, text=element.stared_value, font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.grid(row=i, column=11, sticky="w", padx=10)

            Grid.columnconfigure(element_frame, 0, weight=1)
            Grid.columnconfigure(element_frame, 1)
            Grid.columnconfigure(element_frame, 2)
            Grid.columnconfigure(element_frame, 3, minsize=300)

            j = 0

            while j < 7:
                Grid.columnconfigure(element_frame, 4+j, minsize=90)
                j += 1

            Grid.columnconfigure(element_frame, 11, minsize=150)

            element_frame.pack(fill=X)

            i += 1

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

            self.display()

            self.parent.program_score()

            if self.lastElement:
                comp = BoxElement(ProgramBox({
                    'program': self.box.program,
                    'type': None
                }), self.root, self.parent)
                comp.wrapper()

                self.lastElement = False

    def star(self, element):
        if element.star:
            element.star = 0
        else:
            element.star = 1
        
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
    

# Add a jump element
class JumpElement():

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
        btns = ['W', 'T', 'S', 'F', 'Lz', 'Lo', 'Th', 'A']
        
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


# Add a jump element
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

# Add a step element
class StepElement():

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

                if btn['text'] == 'NSt':
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
        btns = ['NSt', 'StB', 'St1', 'St2', 'St3', 'St4']
        
        frame_step = Frame(self.frame, bg="#0a1526")

        i = 0

        for btnLabel in btns:
            self.btnsBas.append(Button(frame_step, text=btnLabel, font=("sans-serif", 11)))

            if btnLabel == 'NSt':
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


# Add a choreo element
class ChoreoElement():

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

                if btn['text'] == 'NChSt':
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
        btns = ['NChSt', 'ChSt']
        
        frame_step = Frame(self.frame, bg="#0a1526")

        i = 0

        for btnLabel in btns:
            self.btnsBas.append(Button(frame_step, text=btnLabel, font=("sans-serif", 11)))

            if btnLabel == 'NChSt':
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

if __name__ == "__main__":

    # Fist, check integrity before start
    Category.database_integrity()
    ElementType.database_integrity()
    Element.database_integrity()
    Program.database_integrity()
    ProgramElement.database_integrity()
    ProgramBox.database_integrity()
    Session.database_integrity()

    # Then load app
    rollart = RollartApp()
    rollart.home()
    rollart.window.mainloop()
