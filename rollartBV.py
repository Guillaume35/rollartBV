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

import os
from pathlib import Path
from functools import partial
import urllib.request
import urllib.parse

from tkinter import *
from tkinter import messagebox

import tools

from apps.box_element import *
from apps.result_program import *

from apps.scrolled_frame import *

import elements_database
import types_database
from categories_database import *
from sessions_database import *
from skaters_database import *

from motor.program import *
from motor.session import *
from motor.category import *
from motor.element import *
from motor.element_type import *
from motor.program_element import *
from motor.skater import *

from penalty import *
from component import *

#
# RollartApp class
class RollartApp:

    """
    * This is the root application class managing all the main process :
    * Opening main window, starting and judging a program by the data
    * operator and starting all application subprocess.
    """

    def __init__(self):
        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("RollArt Unchained")
        self.window.geometry("1600x900")
        self.window.minsize(1280,720)
        self.window.config(background="#0a1526")

        # Initializing values
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
        self.footer = None

        # Check current session
        # The system is able to open only one session at a time even if the
        # application is started more that once.
        currentSession = Session.getOpened()

        if currentSession:
            self.session = currentSession


    #
    # start()
    # Start a program without any opened session (solo skater mode)
    # This method check if progam fields are filed and start the program if so.
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
    # End of start()


    #
    # start_session()    
    # Start loaded session (competition mode). Works only if a session is loaded.
    # This method show teams score and categories list. It is possible to start category 
    # from that panel, show results for finished categories. Once a category is ended,
    # it is no more possible to add skaters.
    def start_session(self):

        # Clear the root window and add a new empty frame
        self.frame.pack_forget()
        self.frame.destroy()

        self.frame = Frame(self.window, bg="#0a1526")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        # Title frame
        frame = Frame(self.frame, bg="#bd3800")

        label = Label(frame, text="Ready to start !", bg="#bd3800", fg="white", font=("sans-serif", 14), justify=LEFT, padx=10)
        label.grid(row=0, column=1, sticky="nesw", ipadx=5, ipady=10)

        btn = Button(frame, text="Home", font=("sans-serif", 12), command=self.home)
        btn.grid(row=0, column=0, sticky="nesw", ipadx=5, ipady=10)

        frame.grid(row=0, column=0, sticky="nesw")

        # Add a scroll frame for the rest of the elements
        scrollFrame = VerticalScrolledFrame(self.frame, bg="#0a1526")

        scrollFrameIn = scrollFrame.interior
        scrollFrame.interior.configure(bg="#0a1526")
        scrollFrame.canvas.configure(bg="#0a1526")

        #
        # TEAMS TABLE
        # If teams is used (skaters with team value), the system show the score of each team 
        # at the moment of competition. Team score is the addition of the total score of all
        # skaters with the same team name.
        teams = Skater.getTeams(self.session.id)

        if teams:

            if len(teams):

                frame = Frame(scrollFrameIn, bg="#0a1526")

                label = Label(frame, text="Teams score", bg="#0a1526", fg="white", font=("sans-serif", 12, "bold"), justify=LEFT, padx=10)
                label.pack(fill=X)

                frame.pack(fill=X, pady=15)

                frame = Frame(scrollFrameIn, bg="#0a1526")

                i=0

                # For each team, we show the team name and the current score
                for team in teams:

                    label = Label(frame, text=team['team'], bg="#0a1526", fg="white", font=("sans-serif", 12), justify=LEFT, padx=10, borderwidth=1, relief="groove", anchor="w")
                    label.grid(row=0, column=i, sticky="nesw", ipadx=5, ipady=10)

                    label = Label(frame, text=round(team['total_score'],2), bg="#0a1526", fg="white", font=("sans-serif", 12), justify=LEFT, padx=10, borderwidth=1, relief="groove", anchor="w")
                    label.grid(row=1, column=i, sticky="nesw", ipadx=5, ipady=10)

                    Grid.columnconfigure(frame, i, weight=1)

                    i +=1

                frame.pack(fill=X, pady=15)
        # End of TEAMS TABLE
        #

        #
        # CATEGORIES TABLE
        # List all the categories in the defined order and show available options for each one.
        # Options can be : start short, start long, wait long (if short is not ended), results short (if ended), results long (if ended)
        label = Label(scrollFrameIn, text="Categories", bg="#0a1526", fg="white", font=("sans-serif", 12, "bold"), justify=LEFT, padx=10)
        label.pack(fill=X, pady=15)

        frame = Frame(scrollFrameIn, bg="#0a1526")

        categories = self.session.getCategories()

        i=0

        # For each category, we check for possibles options
        for category in categories:

            # Category label includes category name and number of skaters.
            label = Label(frame, text=category.name+ ' ('+str(category.getSkatersNum())+')', bg="#0a1526", fg="white", borderwidth=1, relief="groove", anchor="w", justify=LEFT, font=("sans-serif", 12), padx=10)
            label.grid(row=i, column=0, sticky="nesw", ipadx=10, ipady=10)

            # Button START has the same callback function even for short and long program.
            # START button call the resume_category method which start the category/last program 
            # at the last knowed point. So it is possible to restart a category or a program at
            # computer breakpoint (if so).
            actionStart = partial(self.resume_category, category)

            # If short program
            if category.short > 0:
                
                # Short program can be "UNSTARTED" or running ("SHORT"). All other status value 
                # is concidered as short program end so we can display the results button (else statement)
                if str(category.status).upper() == 'UNSTARTED' or str(category.status).upper() == 'SHORT' or not category.status:
                    btn = Button(frame, text="Start short", font=("sans-serif", 12, "bold"), bg="#bd3800", fg="white", command=actionStart)
                    btn.grid(row=i, column=1, ipadx=10, ipady=10, sticky='nesw')
                
                # Short program ended
                else:

                    action = partial(self.results, category, 'short')
                    btn = Button(frame, text="Short results", font=("sans-serif", 12), bg="PaleGreen1", command=action)
                    btn.grid(row=i, column=1, ipadx=10, ipady=10, sticky='nesw')
                # End of ended statement
            # End of if short program

            # If long program
            if category.long > 0:
                # Long program can be running ("LONG") or ended ("END"). If there is no short program defined 
                # in the category, status can be nothing or END.
                if str(category.status).upper() == 'LONG' or (category.short <= 0 and str(category.status).upper() != 'END'):
                    btn = Button(frame, text="Start long", font=("sans-serif", 12, "bold"), bg="#bd3800", fg="white", command=actionStart)
                    btn.grid(row=i, column=2, ipadx=10, ipady=10, sticky='nesw')
                
                # If long program is END, we propose the results
                elif str(category.status).upper() == 'END':
                    action = partial(self.results, category, 'long')
                    btn = Button(frame, text="Long results", font=("sans-serif", 12), bg="PaleGreen1", command=action)
                    btn.grid(row=i, column=2, ipadx=10, ipady=10, sticky='nesw')

                # In case of short program which is not over in the category, we show a WAIT button for 
                # the long program that indicate short program must be finished first.
                else:
                    actionWait = partial(messagebox.showinfo, title="Can't start", message="Finish short program first")
                    btn = Button(frame, text="Wait long", font=("sans-serif", 12), command=actionWait)
                    btn.grid(row=i, column=2, ipadx=10, ipady=10, sticky='nesw')
                # End of program status statement
            # End of if long program

            i += 1
        # End of for each categories

        Grid.columnconfigure(frame, 0, weight=1)


        frame.pack(fill=X, pady=10)

        # End of CATEGORIES TABLE
        #

        scrollFrame.grid(row=1, column=0, sticky="nesw")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.frame.grid(row=0, column=0, sticky="nesw")
    # End of start_session()


    # 
    # resume_category(category = Category)
    # This method is called for starting or resuming a category if program has been closed while running.
    # The system get the last opened program in the category or the next program of the category.
    # If we are athe the end of the program, window is cleaned and the list of categories is displayed
    # (start_session method)
    def resume_category(self, category):
        # We can open only one category and one program at a time. It is 
        # stored in the root application object
        self.category = category

        skater = category.getCurrentSkater()
        
        # If we have a current skater in the category, we get the program and start it with
        # open_program() method
        if skater:
            skater.status = category.status
            skater.record()
            program = skater.getCurrentProgram()

            self.open_program(program)

        # In the next case, we concider the program as "OVER" for all the category. We update 
        # category status and go the the list of categories with start_session() method.
        else:
            if category.status.upper() == 'SHORT':
                category.status = 'long'
            else:
                category.status = 'end'

            category.record()

            self.start_session()
        # End of skaters check statement
    # End of resume_category()


    # 
    # home()
    # Display the home screen for charging session, starting a program/session, managing and 
    # configuring options, skaters, categories, elements.
    def home(self):

        # Clear the root window and add a new empty frame
        if (self.frame):
            self.frame.pack_forget()
            self.frame.destroy()

        self.frame = Frame(self.window, bg="#0a1526")

        # Title frame
        title_frame = Frame(self.frame, bg="#0a1526")

        label_title = Label(title_frame, text="RollArt Unchained", font=("sans-serif", 24), bg="#0a1526", fg="white")
        label_title.pack()

        label_subtitle = Label(title_frame, text="The free and open source Roll Art system", font=("sans-serif", 14), bg="#0a1526", fg="white")
        label_subtitle.pack()

        title_frame.pack(pady=15)
        # End of title frame

        # Session frame
        session_frame = Frame(self.frame, bg="#0a1526")

        sessionApp = SessionApp(self)

        # If a session is opened, we add a "close session" button
        if self.session:

            label_session = Label(session_frame, text=self.session.name, font=("sans-serif", 12, 'bold'), bg="#0a1526", fg="white")
            label_session.pack(pady=10)

            sessionAction = partial(sessionApp.close_session, self.session)

            sessions_db_btn = Button(session_frame, text="Close session", font=("sans-serif", 12), bg="#cf362b", fg="white", command=sessionAction)
            sessions_db_btn.pack(pady=5, fill=X)

        # No session is started, we propose to open or create a new one
        else:
            sessionAction = partial(sessionApp.open_window)

            sessions_db_btn = Button(session_frame, text="Open session", font=("sans-serif", 12), bg="#dfe7e8", command=sessionAction)
            sessions_db_btn.pack(pady=5, fill=X)
        # End of session statement

        session_frame.pack(pady=15, fill=X)
        # End of session frame

        # Menu frame
        menu_frame = Frame(self.frame, bg="#0a1526")

        #
        # START OPTIONS
        # An error empty label is added to the frame for feedback if needed
        error_frame = Frame(menu_frame, bg="red")
        self.error_label = Label(error_frame, text="", font=("sans-serif", 10), bg="red", fg="white", height=0)
        error_frame.pack()

        # If no session is started, we add a form with skater name and program name with a quick start 
        # button (program only mode). All fields are required. Informations can be whatever data operator
        # wants, there is no check on this mode.
        if not self.session:
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

            # Start button use single program mode method
            actionStart = self.start

        # Session is started, we only display start button which is linked to session mode method
        else:
            actionStart = self.start_session
        # End of check session statement

        start_btn = Button(menu_frame, text="Start", font=("sans-serif", 14, "bold"), bg="#bd3800", fg="white", pady=8, command=actionStart)
        start_btn.pack(pady=10, fill=X)

        # End of START OPTIONS
        #


        #
        # Skaters and categories
        # If a session is opened, we add options in the menu to manage categories and skaters list
        if self.session:
            label = Label(menu_frame, text="Current session managment", font=("sans-serif", 12), bg="#0a1526", fg="white")
            label.pack(pady=10)

            categoryApp = CategoryApp(self)

            btn = Button(menu_frame, text="Categories", font=("sans-serif", 12), bg="#dfe7e8", command=categoryApp.open_window)
            btn.pack(pady=5, fill=X)

            btn = Button(menu_frame, text="Skaters", font=("sans-serif", 12), bg="#dfe7e8", command=self.skater_database)
            btn.pack(pady=5, fill=X)
        # End of session check statement

        # End of skaters and categories
        #


        #
        # Configuration
        # We propose to configure roll art system and application
        label = Label(menu_frame, text="RollArt configuration", font=("sans-serif", 12), bg="#0a1526", fg="white")
        label.pack(pady=10)

        elements_db_btn = Button(menu_frame, text="Elements database", font=("sans-serif", 12), bg="#dfe7e8", command=elements_database.open_window)
        elements_db_btn.pack(pady=5, fill=X)

        # TODO : this section has some bugs and has been disabled
        # types_db_btn = Button(menu_frame, text="Types database", font=("sans-serif", 12), bg="#dfe7e8", command=types_database.open_window)
        # types_db_btn.pack(pady=5, fill=X)

        # End of configuration
        #

        menu_frame.pack(pady=15, fill=X)
        # End of menu

        # add to window
        self.frame.pack(expand=YES)
    # End of home()


    #
    # open_program(program = Program)
    # This method open a specific program after initial check. This is the program recorder mode
    # which let the data operator to enter all the elements called by the technical specialist
    # and its assistant.
    # The system is also able to communicated in real time with a server all the results.
    def open_program(self, program):

        self.program = program

        # Clear the window and create new empty frame
        if self.frame:
            self.frame.destroy()

        self.frame = Frame(self.window, bg="#0a1526")

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        #
        # Title frame
        # It display home button, title, skaters and program name which will be controled by
        # the data operator and assistant.
        title_frame = Frame(self.frame, bg="#bd3800")

        btn = Button(title_frame, text="Home", font=("sans-serif", 12), command=self.home)
        btn.grid(row=0, column=0, sticky="nsew")

        label_title = Label(title_frame, text="Record program", font=("sans-serif", 18), bg="#bd3800", fg="white", padx=10)
        label_title.grid(row=0, column=1, sticky="nsw")

        label_skater = Label(title_frame, text=self.program.skater+' ('+program.program_name+')', font=("sans-serif", 10), bg="#bd3800", fg="white", padx=10)
        label_skater.grid(row=0, column=2, sticky="nes")

        Grid.rowconfigure(title_frame, 0, weight=1)
        Grid.columnconfigure(title_frame, 1, weight=1)

        title_frame.grid(row=0, column=0, sticky="nesw")
        # End of title frame
        #


        # 
        # BOX LIST
        # Box are the containers in which elements are recorded. It is the sequence of the 
        # program order by specialist or assistant call. Boxes is used to enter the type of
        # element (ex : SoloJump)

        # Add a scroll frame for box list
        scrollFrame = VerticalScrolledFrame(self.frame, bg="#0a1526")

        scrollFrameIn = scrollFrame.interior
        scrollFrame.interior.configure(bg="#0a1526")
        scrollFrame.canvas.configure(bg="#0a1526")

        self.boxes_frame = Frame(scrollFrameIn,  bg="#0a1526")

        boxes = self.program.getBoxes()

        createEmpty = True

        if len(boxes):
            lastCreated = boxes[-1]
            elements = lastCreated.getElements()

            # If the last box have no elements, it is not needed to create an empty one.
            if not len(elements):
                createEmpty = False
        # End of check boxes statement

        # If the program is not START (so it might be END), we dont create empty box cause 
        # there is no new element to record.
        if self.program.status.upper() != 'START':
            createEmpty = False
        
        # We add an empty box to the list
        if createEmpty:
            boxes.append(ProgramBox({
                'program': self.program.id
            }))

        i = 0

        # For each box added in the previous list, we create a box app in charge of displaying,
        # calculating and managing the elements contained in the box.
        self.boxes = []

        for box in boxes:

            comp = BoxElement(box, self.boxes_frame, self)
            comp.wrapper()

            self.boxes.append(comp)

            i += 1
        # End of foreach boxes

        self.boxes_frame.pack(fill=X)

        scrollFrame.grid(row=1, column=0, sticky="nesw")

        # End of BOX LIST
        #


        # FOOTER
        self.footer = Frame(self.frame, bg="#0a1526")


        #
        # FOOTER TOOLBAR
        # We add all options for the global managment of the program : start/stop, penalty, next skater, skip...
        toolbar = Frame(self.footer, bg="#0a1526")

        btn = Button(toolbar, text=str(self.program.fall)+" Fall", font=("sans-serif", 14, "bold"), bg="DarkOrange2", fg="white", pady=12)
        action = partial(self.program_fall, btn)
        btn.configure(command=action)
        btn.grid(row=0, column=0, pady=10, sticky="nsew")

        btn = Button(toolbar, text="Penalty", font=("sans-serif", 14, "bold"), bg="DarkOrange2", fg="white", pady=12, command=self.program_penalty)
        btn.grid(row=0, column=1, pady=10, sticky="nsew")

        # Check program status in order to write START or STOP on the program button
        if self.program.status.upper() == 'START':
            label = 'STOP'
            color = 'red'
        else:
            label = 'START'
            color = 'green'
        # End of program status statement


        btn = Button(toolbar, text=label, font=("sans-serif", 14, "bold"), bg=color, fg="white", pady=12)
        action = partial(self.toggle_program_status, btn)
        btn.configure(command=action)
        btn.grid(row=0, column=2, pady=10, sticky="nsew")

        # If session is opened, we add options to control the category
        if self.program.session:

            # Next skater will check if values are fullfiled and display an alert box if not.
            action = partial(self.confirm_skater)
            btn = Button(toolbar, text="Next skater", font=("sans-serif", 14, "bold"), bg="green", fg="white", pady=12, command=action)
            btn.grid(row=0, column=3, pady=10, sticky="nsew")

            # Skip will allow to go to the next skater even if no values are filled.
            btn = Button(toolbar, text="Skip", font=("sans-serif", 14, "bold"), bg="DarkOrange2", fg="white", pady=12, command=self.skip_skater)
            btn.grid(row=0, column=4, pady=10, sticky="nsew")
        # End of check session statement

        Grid.columnconfigure(toolbar, 2, weight=1)

        toolbar.pack(fill=X, pady=10)

        # End of FOOTER TOOLBAR
        #


        # 
        # COMPONENTS
        # Components can be added by data operator directly after beeing called by a judge.
        components = ['skating_skills', 'transitions', 'choreography', 'performance']

        combar = Frame(self.footer, bg="#0a1526")

        i = 0

        # For each component label we add a button with name and current value for the program.
        # If component is undefined (=0), value is in red and "Next skater" button will not accept
        # to continue until all components values are fullfiled.
        for component in components:
            action = partial(self.program_component,component)

            btn = Button(combar, text=component, font=("sans-serif", 14), pady=10, command=action)
            btn.grid(row=0, column=i, pady=10, sticky="nsew")
            self.btnsComponents[component] = btn
            self.program_component_value(component)

            Grid.columnconfigure(combar, i, weight=1)

            i+=1
        # End of components label loop

        combar.pack(fill=X)
        
        # End of COMPONENTS
        #

        #
        # SERVER EXCHANGE
        # We send information about the current skater to a HTTP server for a realtime name and results display
        skaterTeam = ''

        # If we use session, we add team name
        if self.program.session and self.program.skater_id:
            skater = Skater(self.program.skater_id)
            skaterTeam = skater.team
        # End of session statement

        skaterName = urllib.parse.quote_plus(self.program.skater)

        url = 'https://www.raiv.fr/wintercup2020/data.php?skaterName='+skaterName+'&skaterTeam='+skaterTeam+'&liveScoreEl=-&liveScoreVal=0.0&liveScoreSk=0.0&finalScoreTechnical=0.0&finalScoreComponents=0.0&finalScoreDeduction=0.0&segmentScore=0.0&finalScore=0.0&rank=0'
        urllib.request.urlopen(url)
        # End of SERVER EXCHANGE
        #

        # Calling program score footer
        self.program_score()

        self.footer.grid(row=2, column=0, sticky="nesw")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)

        self.frame.grid(row=0, column=0, sticky="nesw")
    # End of open_program()


    #
    # program_score()
    # Calculate and show the current program technical score, components, penalization, total score.
    def program_score(self):
        
        # Clearing the last frame
        if self.score_frame:
            self.score_frame.destroy()

        self.score_frame = Frame(self.footer,  bg="#0a1526")

        # Refresh program score and record
        self.program.calculate()
        self.program.record()

        # For each type of score, show one row with label and score
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

        # End of score table

        #
        # SERVER EXCHANGE
        # We send information about the current skater to a HTTP server for a realtime name and results display
        rank = 1
        teamScore = 0
        team = 'team'
        
        # If session is opened, we get the current rank of the skater in the category and calculate
        # team score
        if self.program.session:
            rank = self.program.getRank()

            skater = Skater(self.program.skater_id)

            teamScore = skater.getTeamScore()
            team = 'team'+skater.team
        # End of check session statement

        url = 'https://www.raiv.fr/wintercup2020/data.php?liveScoreSk='+str(self.program.total_score)+'&finalScoreTechnical='+str(self.program.technical_score)+'&finalScoreComponents='+str(self.program.components_score)+'&finalScoreDeduction='+str(self.program.penalization)+'&segmentScore='+str(self.program.score)+'&finalScore='+str(self.program.total_score)+'&rank='+str(rank)+'&'+team+'='+str(teamScore)
        urllib.request.urlopen(url)

        # End of SERVER EXCHANGE
        #

        self.score_frame.pack(fill=X, pady=10)
    # End of program_score()


    #
    # toggle_program_status(btn = Button)
    # Change the program status to START or STOP (depending on the previous status)
    def toggle_program_status(self, btn):
        # If program is started, we change status to STOP and change button appearance.
        # Toggle last box to display mode or remove
        if self.program.status.upper() == 'START':
            self.program.status = 'stop'
            label = 'START'
            color = 'green'

            # Check if last box is empty and delete it if so
            lastCreated = self.boxes[-1]
            if lastCreated:
                elements = lastCreated.box.getElements()

                if not len(elements):
                    lastCreated.box.delete()
                    lastCreated.frame.destroy()

                else:
                    if lastCreated.mode != 'display':
                        lastCreated.display()
            # End of check last box empty

        # Program is stopped, we change to START and change button appearance.
        # Add a new box in form mode in order to record new element if needed
        else:
            self.program.status = 'start'
            label = 'STOP'
            color = 'red'

            comp = BoxElement(ProgramBox({
                'program': self.program.id
            }), self.boxes_frame, self)
            comp.wrapper()

            self.boxes.append(comp)
        # End of check status
        
        self.program.record()

        btn.configure(bg=color, text=label)
    # End toggle_program_status()


    # 
    # program_fall(btn = Button)
    # Add a fall, increment the button, apply penalty
    def program_fall(self, btn):
        self.program.fall += 1
        self.program.penalization -= 1
        self.program.record()

        self.program_score()

        btn.configure(text=str(self.program.fall)+" Fall")
    # End of program_fall()

    #
    # program_penalty()
    # Open penalty dialog box
    def program_penalty(self):
        penaltyApp = PenaltyApp(self)
        penaltyApp.open_window()
    # End of program_penalty()

    # 
    # program_component(component = String)
    # Open component dialog box
    def program_component(self, component):
        componentApp = ComponentApp(component, self)
        self.componentsApps.append(componentApp)
        componentApp.open_window()
    # End of program_component()


    #
    # program_component_value(component = String)
    # Update component button with a new value. Toggle btn appearance depending on
    # component value (if <= 0, color is red)
    def program_component_value(self, component):

        programData = self.program.getAll()
        val = programData[component]
        btn = self.btnsComponents[component]

        if val > 0 and val <= 10:
            btn.configure(fg="black", text=component+' '+str(val))
        else:
            btn.configure(fg="red", text=component+' '+str(val))
    # End of program_component_value()


    #
    # skater_database()
    # Edit skaters list for the current session
    def skater_database(self):

        # Create main window
        window = Tk()

        # Customizing window
        window.title("Skaters - RollArt BV")
        window.geometry("1280x720")
        window.minsize(1280,720)
        window.config(background="#0a1526")

        # Categories frame
        frame = Frame(window, bg="")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Add a scroll frame for box list
        scrollFrame = VerticalScrolledFrame(frame, bg="#0a1526")

        scrollFrameIn = scrollFrame.interior
        scrollFrame.interior.configure(bg="#0a1526")
        scrollFrame.canvas.configure(bg="#0a1526")

        label = Label(scrollFrameIn, text="Skaters", font=("sans-serif", 18), fg="white", bg="#0a1526")
        label.pack(fill=X, pady=15)

        categories = self.session.getCategories()

        # Foreach category, a button is created to edit skaters list
        for category in categories:

            skaterApp = SkaterApp(self, category)

            btn = Button(scrollFrameIn, text=category.name, font=("sans-serif", 12), command=skaterApp.open_window, pady=8)
            btn.pack(fill=X, pady=8)
        # End of categories loop

        scrollFrame.grid(row=0, column=0, sticky="nesw")

        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)

        frame.grid(row=0, column=0, sticky="nesw")

        window.mainloop()
    # End of skater_database()


    #
    # confirm_skater()
    # Method called when data operator click on Next skater
    # This method control if all mandatories values on the current program are set before confirmation of the
    # program. If not, an alert is raised.
    def confirm_skater(self):

        # Program status has to be "STOP"
        if self.program.status.upper() == 'STOP':
            
            # Components must be applied
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
            # End of components check
        
        # Program status is not "STOP"
        else:
            messagebox.showwarning(title="Can't confirm", message="Stop program before confirm")
        # End of program status check
    # End of confirm_skater()


    #
    # skip_skater()
    # Like confirm_skater, this method go to the next skater in the category but without any
    # control on the values. Program can be empty or not to be skiped.
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
    # End of skip_skater()


    #
    # close_components_windows()
    # Close all components windows and reset componentsApp before going to the next skater
    def close_components_windows(self):
        for app in self.componentsApps:
            if not app.closed:
                app.close_window()

        self.componentsApps = []
    # End of close_components_windows()


    #
    # results(category = Category, programType = String)
    # If a session is opened, show the result of a program. If it is the long/only program, it show the 
    # total score and the final rank for each skaters in the category
    #
    # Matrice of short program or long progam only
    # | Rank | Skater | Tech. score | Components | Deduction | Total |
    #
    # Matric of long program with short program on the category
    # | Rank | Skater | Tech. score | Components | Deduction | Program | Total |
    def results(self, category, programType):
        # Create main window
        window = Tk()

        # Customizing window
        window.title("Results - "+category.name+" - "+programType+" - RollArt BV")
        window.geometry("1600x720")
        window.minsize(1600,720)
        window.config(background="#0a1526")

        # List frame
        frame = Frame(window, bg="")

        label = Label(frame, text="Results - "+category.name+" - "+programType, font=("sans-serif", 14), fg="white", bg="#0a1526")
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

        # If there is more than one program (short and long), the label for the score is "Program".
        if category.short > 0 and category.long > 0:
            text = 'Program'
        # In the other case, there is only one program, the score of the program is also the total score
        else:
            text = 'Total'
        # End of number of program check

        label = Label(frame, text=text, font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
        label.grid(row=i, column=5, sticky="nsew")

        # If there is a short program and we display the result of long program, we add a total column to the table
        if category.short > 0 and programType.upper() == 'LONG':
            label = Label(frame, text="Total", font=("sans-serif", 12, "bold"), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
            label.grid(row=i, column=6, sticky="nsew")
        # End of check if long with total column added

        programs = category.getResults(programType)

        # For each program, we display the results according the matrice
        for program in programs:
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

            col = 6

            if category.short > 0 and programType.upper() == 'LONG':
                label = Label(frame, text=program.total_score, font=("sans-serif", 12), padx=10, pady=10, borderwidth=1, relief="groove", bg="#0a1526", fg="white", justify=LEFT,  anchor="w")
                label.grid(row=i+1, column=col, sticky="nsew")
                col += 1
            
            action = partial(self.result_program, program)
            btn = Button(frame, text="Details", font=("sans-serif", 12), command=action)
            btn.grid(row=i+1, column=col, sticky="nsew")

            i +=1
        # End of programs loop

        Grid.columnconfigure(frame, 0, minsize=100)
        Grid.columnconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 2, minsize=250)
        Grid.columnconfigure(frame, 3, minsize=250)
        Grid.columnconfigure(frame, 4, minsize=120)
        Grid.columnconfigure(frame, 5, minsize=250)

        col = 6

        if category.short > 0 and programType.upper() == 'LONG':
            Grid.columnconfigure(frame, col, minsize=250)
            col += 1

        frame.pack(fill=X)
        # End of list frame
            

        window.mainloop()
    # End of results()


    #
    # result_program(program = Program)
    # Open result program application to display details on new window
    def result_program(self, program):
        resultApp = ResultProgramApp(program)
        resultApp.open_window()
    # End of result_program()

if __name__ == "__main__":

    # Check if we have a working directory for the application
    home_path = str(Path.home())
    if not os.path.exists(home_path+'/.rollartBV'):
        os.makedirs(home_path+'/.rollartBV')


    # Check database integrity before start
    Category.database_integrity()
    ElementType.database_integrity()
    Element.database_integrity()
    Program.database_integrity()
    ProgramElement.database_integrity()
    ProgramBox.database_integrity()
    Session.database_integrity()
    Skater.database_integrity()

    # Load the app
    rollart = RollartApp()
    rollart.home()
    rollart.window.mainloop()
