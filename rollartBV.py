from tkinter import *
from tkinter import messagebox
import elements_database
import types_database
from categories_database import *
from sessions_database import *
from skaters_database import *
from functools import partial
from motor.program import *
from motor.session import *
from motor.category import *
from motor.element import *
from motor.element_type import *
from motor.program_element import *
from motor.skater import *
import tools
from penalty import *
from component import *
import urllib.request
import urllib.parse

class RollartApp:

    def __init__(self):
        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("RollArt Free2Skate")
        self.window.geometry("1600x900")
        self.window.minsize(1280,720)
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
        self.boxes = []
        self.btnsComponents = {
            'skating_skills': None,
            'transitions': None,
            'choreography': None,
            'performance': None
        }
        self.session = None
        self.category = None
        self.componentsApps = []

        # check current session
        currentSession = Session.getOpened()

        if currentSession:
            self.session = currentSession


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

            self.open_program(program)

    
    # Start a session
    def start_session(self):

        self.frame.pack_forget()
        self.frame.destroy()

        self.frame = Frame(self.window, bg="#0a1526")

        frame = Frame(self.frame, bg="#bd3800")

        label = Label(frame, text="Ready to start !", bg="#bd3800", fg="white", font=("sans-serif", 14), justify=LEFT, padx=10)
        label.grid(row=0, column=1, sticky="nesw", ipadx=5, ipady=10)

        btn = Button(frame, text="Home", font=("sans-serif", 12), command=self.home)
        btn.grid(row=0, column=0, sticky="nesw", ipadx=5, ipady=10)

        frame.pack(fill=X)

        teams = Skater.getTeams(self.session.id)

        if teams:

            if len(teams):

                frame = Frame(self.frame, bg="#0a1526")

                label = Label(frame, text="Teams score", bg="#0a1526", fg="white", font=("sans-serif", 12, "bold"), justify=LEFT, padx=10)
                label.pack(fill=X)

                frame.pack(fill=X, pady=15)

                frame = Frame(self.frame, bg="#0a1526")

                i=0

                for team in teams:

                    label = Label(frame, text=team['team'], bg="#0a1526", fg="white", font=("sans-serif", 12), justify=LEFT, padx=10, borderwidth=1, relief="groove", anchor="w")
                    label.grid(row=0, column=i, sticky="nesw", ipadx=5, ipady=10)

                    label = Label(frame, text=round(team['total_score'],2), bg="#0a1526", fg="white", font=("sans-serif", 12), justify=LEFT, padx=10, borderwidth=1, relief="groove", anchor="w")
                    label.grid(row=1, column=i, sticky="nesw", ipadx=5, ipady=10)

                    Grid.columnconfigure(frame, i, weight=1)

                    i +=1

                frame.pack(fill=X, pady=15)

        label = Label(self.frame, text="Categories", bg="#0a1526", fg="white", font=("sans-serif", 12, "bold"), justify=LEFT, padx=10)
        label.pack(fill=X, pady=15)

        frame = Frame(self.frame, bg="#0a1526")

        categories = self.session.getCategories()

        i=0

        for category in categories:
            label = Label(frame, text=category.name+ ' ('+str(category.getSkatersNum())+')', bg="#0a1526", fg="white", borderwidth=1, relief="groove", anchor="w", justify=LEFT, font=("sans-serif", 12), padx=10)
            label.grid(row=i, column=0, sticky="nesw", ipadx=10, ipady=10)

            actionStart = partial(self.resume_category, category)

            if category.short > 0:

                if str(category.status).upper() == 'UNSTARTED' or str(category.status).upper() == 'SHORT' or not category.status:
                    btn = Button(frame, text="Start short", font=("sans-serif", 12, "bold"), bg="#bd3800", fg="white", command=actionStart)
                    btn.grid(row=i, column=1, ipadx=10, ipady=10, sticky='nesw')
                else:

                    action = partial(self.results, category, 'short')
                    btn = Button(frame, text="Short results", font=("sans-serif", 12), bg="PaleGreen1", command=action)
                    btn.grid(row=i, column=1, ipadx=10, ipady=10, sticky='nesw')

            if category.long > 0:
                if str(category.status).upper() == 'LONG' or (category.short <= 0 and str(category.status).upper() != 'END'):
                    btn = Button(frame, text="Start long", font=("sans-serif", 12, "bold"), bg="#bd3800", fg="white", command=actionStart)
                    btn.grid(row=i, column=2, ipadx=10, ipady=10, sticky='nesw')
                elif str(category.status).upper() == 'END':
                    action = partial(self.results, category, 'long')
                    btn = Button(frame, text="Long results", font=("sans-serif", 12), bg="PaleGreen1", command=action)
                    btn.grid(row=i, column=2, ipadx=10, ipady=10, sticky='nesw')
                else:
                    actionWait = partial(messagebox.showinfo, title="Can't start", message="Finish short program first")
                    btn = Button(frame, text="Wait long", font=("sans-serif", 12), command=actionWait)
                    btn.grid(row=i, column=2, ipadx=10, ipady=10, sticky='nesw')
            i += 1

        Grid.columnconfigure(frame, 0, weight=1)


        frame.pack(fill=X, pady=10)

        self.frame.pack(fill=X)

    # Resume a category
    def resume_category(self, category):
        self.category = category

        skater = category.getCurrentSkater()
        
        if skater:
            skater.status = category.status
            skater.record()
            program = skater.getCurrentProgram()

            self.open_program(program)

        else:
            if category.status.upper() == 'SHORT':
                category.status = 'long'
            else:
                category.status = 'end'

            category.record()

            self.start_session()


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
        label_title = Label(title_frame, text="RollArt Free2Skate", font=("sans-serif", 24), bg="#0a1526", fg="white")
        label_title.pack()

        label_subtitle = Label(title_frame, text="The free and open source Roll Art system", font=("sans-serif", 14), bg="#0a1526", fg="white")
        label_subtitle.pack()

        sessionApp = SessionApp(self)

        # current session exists
        if self.session:

            label_session = Label(session_frame, text=self.session.name, font=("sans-serif", 12, 'bold'), bg="#0a1526", fg="white")
            label_session.pack(pady=10)

            sessionAction = partial(sessionApp.close_session, self.session)

            sessions_db_btn = Button(session_frame, text="Close session", font=("sans-serif", 12), bg="#cf362b", fg="white", command=sessionAction)
            sessions_db_btn.pack(pady=5, fill=X)

        else:
            sessionAction = partial(sessionApp.open_window)

            # Session menu
            sessions_db_btn = Button(session_frame, text="Open session", font=("sans-serif", 12), bg="#dfe7e8", command=sessionAction)
            sessions_db_btn.pack(pady=5, fill=X)

        # menu
        error_frame = Frame(menu_frame, bg="red")
        self.error_label = Label(error_frame, text="", font=("sans-serif", 10), bg="red", fg="white", height=0)
        error_frame.pack()

        if not self.session:
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

            # Buttons
            start_btn = Button(menu_frame, text="Start", font=("sans-serif", 14, "bold"), bg="#bd3800", fg="white", pady=8, command=self.start)
            start_btn.pack(pady=10, fill=X)

        else:

            # Buttons
            start_btn = Button(menu_frame, text="Start", font=("sans-serif", 14, "bold"), bg="#bd3800", fg="white", pady=8, command=self.start_session)
            start_btn.pack(pady=10, fill=X)

        

        # Managing skaters list
        if self.session:
            label = Label(menu_frame, text="Current session managment", font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.pack(pady=10)

            categoryApp = CategoryApp(self)

            btn = Button(menu_frame, text="Categories", font=("sans-serif", 12), bg="#dfe7e8", command=categoryApp.open_window)
            btn.pack(pady=5, fill=X)

            btn = Button(menu_frame, text="Skaters", font=("sans-serif", 12), bg="#dfe7e8", command=self.skater_database)
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

        self.program = program

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

        btn = Button(title_frame, text="Home", font=("sans-serif", 12), command=self.home)
        btn.grid(row=0, column=0, sticky="nsew")

        # title
        label_title = Label(title_frame, text="Record program", font=("sans-serif", 18), bg="#bd3800", fg="white", padx=10)
        label_title.grid(row=0, column=1, sticky="nsw")

        label_skater = Label(title_frame, text=self.program.skater+' ('+program.program_name+')', font=("sans-serif", 10), bg="#bd3800", fg="white", padx=10)
        label_skater.grid(row=0, column=2, sticky="nes")

        Grid.rowconfigure(title_frame, 0, weight=1)
        Grid.columnconfigure(title_frame, 1, weight=1)

        # add to window
        title_frame.pack(ipady=5, fill=X)

        boxes = self.program.getBoxes()

        createEmpty = True

        if len(boxes):
            lastCreated = boxes[-1]
            elements = lastCreated.getElements()

            if not len(elements):
                createEmpty = False

        if self.program.status.upper() != 'START':
            createEmpty = False
        
        if createEmpty:
            boxes.append(ProgramBox({
                'program': self.program.id
            }))

        i = 0

        self.boxes = []

        for box in boxes:

            comp = BoxElement(box, self.boxes_frame, self)
            comp.wrapper()

            self.boxes.append(comp)

            i += 1

        #self.program_element_form()
        self.boxes_frame.pack(fill=X)

        toolbar = Frame(self.frame, bg="#0a1526")

        btn = Button(toolbar, text=str(self.program.fall)+" Fall", font=("sans-serif", 14, "bold"), bg="DarkOrange2", fg="white", pady=12)
        action = partial(self.program_fall, btn)
        btn.configure(command=action)
        btn.grid(row=0, column=0, pady=10, sticky="nsew")

        btn = Button(toolbar, text="Penalty", font=("sans-serif", 14, "bold"), bg="DarkOrange2", fg="white", pady=12, command=self.program_penalty)
        btn.grid(row=0, column=1, pady=10, sticky="nsew")

        if self.program.status.upper() == 'START':
            label = 'STOP'
            color = 'red'
        else:
            label = 'START'
            color = 'green'


        btn = Button(toolbar, text=label, font=("sans-serif", 14, "bold"), bg=color, fg="white", pady=12)
        action = partial(self.toggle_program_status, btn)
        btn.configure(command=action)
        btn.grid(row=0, column=2, pady=10, sticky="nsew")

        if self.program.session:

            action = partial(self.confirm_skater)
            btn = Button(toolbar, text="Next skater", font=("sans-serif", 14, "bold"), bg="green", fg="white", pady=12, command=action)
            btn.grid(row=0, column=3, pady=10, sticky="nsew")

            btn = Button(toolbar, text="Skip", font=("sans-serif", 14, "bold"), bg="DarkOrange2", fg="white", pady=12, command=self.skip_skater)
            btn.grid(row=0, column=4, pady=10, sticky="nsew")

        Grid.columnconfigure(toolbar, 2, weight=1)

        toolbar.pack(fill=X, pady=10)

        components = ['skating_skills', 'transitions', 'choreography', 'performance']

        combar = Frame(self.frame, bg="#0a1526")

        i = 0

        for component in components:
            action = partial(self.program_component,component)

            btn = Button(combar, text=component, font=("sans-serif", 14), pady=10, command=action)
            btn.grid(row=0, column=i, pady=10, sticky="nsew")
            self.btnsComponents[component] = btn
            self.program_component_value(component)

            Grid.columnconfigure(combar, i, weight=1)

            i+=1

        combar.pack(fill=X)

        skaterTeam = ''

        if self.program.session and self.program.skater_id:
            skater = Skater(self.program.skater_id)
            skaterTeam = skater.team

        skaterName = urllib.parse.quote_plus(self.program.skater)

        url = 'https://www.raiv.fr/wintercup2020/data.php?skaterName='+skaterName+'&skaterTeam='+skaterTeam+'&liveScoreEl=-&liveScoreVal=0.0&liveScoreSk=0.0&finalScoreTechnical=0.0&finalScoreComponents=0.0&finalScoreDeduction=0.0&segmentScore=0.0&finalScore=0.0&rank=0'
        urllib.request.urlopen(url)

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

        rank = 1
        teamScore = 0
        team = 'team'

        if self.program.session:
            rank = self.program.getRank()

            skater = Skater(self.program.skater_id)

            teamScore = skater.getTeamScore()
            team = 'team'+skater.team

        url = 'https://www.raiv.fr/wintercup2020/data.php?liveScoreSk='+str(self.program.total_score)+'&finalScoreTechnical='+str(self.program.technical_score)+'&finalScoreComponents='+str(self.program.components_score)+'&finalScoreDeduction='+str(self.program.penalization)+'&segmentScore='+str(self.program.score)+'&finalScore='+str(self.program.total_score)+'&rank='+str(rank)+'&'+team+'='+str(teamScore)
        urllib.request.urlopen(url)

        self.score_frame.pack(fill=X, pady=10)

    # Stop program
    def toggle_program_status(self, btn):
        if self.program.status.upper() == 'START':
            self.program.status = 'stop'
            label = 'START'
            color = 'green'

            #check last box and delete
            lastCreated = self.boxes[-1]
            if lastCreated:
                elements = lastCreated.box.getElements()

                if not len(elements):
                    lastCreated.box.delete()
                    lastCreated.frame.destroy()

                else:
                    if lastCreated.mode != 'display':
                        lastCreated.display()

        else:
            self.program.status = 'start'
            label = 'STOP'
            color = 'red'

            comp = BoxElement(ProgramBox({
                'program': self.program.id
            }), self.boxes_frame, self)
            comp.wrapper()

            self.boxes.append(comp)
        
        self.program.record()

        btn.configure(bg=color, text=label)

    # add a fall
    def program_fall(self, btn):
        self.program.fall += 1
        self.program.penalization -= 1
        self.program.record()

        self.program_score()

        btn.configure(text=str(self.program.fall)+" Fall")

    # Open penalty dialog box
    def program_penalty(self):
        penaltyApp = PenaltyApp(self)
        penaltyApp.open_window()

    # Open component dialog
    def program_component(self, component):
        componentApp = ComponentApp(component, self)

        self.componentsApps.append(componentApp)

        componentApp.open_window()

    # Check program component value
    def program_component_value(self, component):

        programData = self.program.getAll()
        val = programData[component]
        btn = self.btnsComponents[component]

        if val > 0 and val <= 10:
            btn.configure(fg="black", text=component+' '+str(val))
        else:
            btn.configure(fg="red", text=component+' '+str(val))

    # Open skaters category window
    def skater_database(self):

        # Create main window
        window = Tk()

        # Customizing window
        window.title("Skaters - RollArt BV")
        window.geometry("1280x720")
        window.minsize(1280,720)
        window.config(background="#0a1526")

        frame = Frame(window, bg="")

        label = Label(frame, text="Skaters", font=("sans-serif", 18), fg="white", bg="#0a1526")
        label.pack(fill=X, pady=15)

        categories = self.session.getCategories()

        for category in categories:

            skaterApp = SkaterApp(self, category)

            btn = Button(frame, text=category.name, font=("sans-serif", 12), command=skaterApp.open_window, pady=8)
            btn.pack(fill=X, pady=8)

        frame.pack(fill=X)

        window.mainloop()

    def confirm_skater(self):

        if self.program.status.upper() == 'STOP':

            if self.program.skating_skills > 0 and self.program.transitions > 0 and self.program.choreography > 0 and self.program.performance > 0:

                self.close_components_windows()
                
                skater = Skater(self.program.skater_id)

                if self.program.program_name.upper() == 'SHORT':
                    status = 'shortend'
                    skater.short_score = self.program.score
                else:
                    status = 'longend'
                    skater.long_score = self.program.score

                skater.status = status
                skater.calculate()
                skater.record()

                self.resume_category(self.category)

            else:
                messagebox.showwarning(title="Can't confirm", message="Asign components values before confirm")
        
        else:
            messagebox.showwarning(title="Can't confirm", message="Stop program before confirm")

    def skip_skater(self):

        if self.program.status.upper() == 'STOP':

            self.close_components_windows()
            
            skater = Skater(self.program.skater_id)

            if self.program.program_name.upper() == 'SHORT':
                status = 'shortend'
                skater.short_score = self.program.score
            else:
                status = 'longend'
                skater.long_score = self.program.score

            skater.status = status
            skater.calculate()
            skater.record()

            self.resume_category(self.category)

        else:
            messagebox.showwarning(title="Can't skip", message="Stop program before skip")

    def close_components_windows(self):
        for app in self.componentsApps:
            if not app.closed:
                app.close_window()

        self.componentsApps = []

    def results(self, category, programType):
        # Create main window
        window = Tk()

        # Customizing window
        window.title("Results - "+category.name+" - "+programType+" - RollArt BV")
        window.geometry("1280x720")
        window.minsize(1280,720)
        window.config(background="#0a1526")

        frame = Frame(window, bg="")

        label = Label(frame, text="Results - "+category.name+" - "+programType, font=("sans-serif", 18), fg="white", bg="#0a1526")
        label.pack(fill=X, pady=15)

        frame.pack(fill=X)

        frame = Frame(window, bg="")

        i = 0

        label = Label(frame, text="Rank", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
        label.grid(row=i, column=0, sticky="nsew")

        label = Label(frame, text="Skater", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
        label.grid(row=i, column=1, sticky="nsew")

        label = Label(frame, text="Tech. score", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT, anchor="w")
        label.grid(row=i, column=2, sticky="nsew")

        label = Label(frame, text="Components", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
        label.grid(row=i, column=3, sticky="nsew")

        label = Label(frame, text="Deduc.", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
        label.grid(row=i, column=4, sticky="nsew")

        if category.short > 0 and category.long > 0:
            text = 'Program'
        else:
            text = 'Total'

        label = Label(frame, text=text, font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
        label.grid(row=i, column=5, sticky="nsew")

        if category.short > 0 and programType.upper() == 'LONG':
            label = Label(frame, text="Total", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i, column=6, sticky="nsew")

        programs = category.getResults(programType)

        for program in programs:
            #program.calculate()
            #program.record()
            label = Label(frame, text=str(i+1), font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i+1, column=0, sticky="nsew")

            label = Label(frame, text=program.skater, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i+1, column=1, sticky="nsew")

            label = Label(frame, text=program.technical_score, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT, anchor="w")
            label.grid(row=i+1, column=2, sticky="nsew")

            label = Label(frame, text=program.components_score, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i+1, column=3, sticky="nsew")

            label = Label(frame, text=program.penalization, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i+1, column=4, sticky="nsew")

            if category.short <= 0 and programType.upper() == 'LONG':
                score = program.total_score
            else:
                score = program.score

            label = Label(frame, text=score, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i+1, column=5, sticky="nsew")

            if category.short > 0 and programType.upper() == 'LONG':
                label = Label(frame, text=program.total_score, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
                label.grid(row=i+1, column=6, sticky="nsew")

            i +=1

        Grid.columnconfigure(frame, 0, minsize=100)
        Grid.columnconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 2, minsize=250)
        Grid.columnconfigure(frame, 3, minsize=250)
        Grid.columnconfigure(frame, 4, minsize=120)
        Grid.columnconfigure(frame, 5, minsize=250)

        if category.short > 0 and programType.upper() == 'LONG':
            Grid.columnconfigure(frame, 6, minsize=250)

        frame.pack(fill=X)
            

        window.mainloop()

            
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

            action = partial(self.time, element)

            btn = Button(element_frame, text="T", font=("sans-serif", 11), command=action)

            if element.time:
                btn.configure(bg='yellow', fg='red')
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
    Skater.database_integrity()

    # Then load app
    rollart = RollartApp()
    rollart.home()
    rollart.window.mainloop()
