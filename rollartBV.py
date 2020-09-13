from tkinter import *
import elements_database
from motor.program import *

# Create main window
window = Tk()

# Customizing window
window.title("RollArt BV")
window.geometry("500x720")
window.minsize(480,360)
window.config(background="#0a1526")

frame = None
skater_entry = None
program_entry = None
error_label = None
element_i = 1


#start program
def start():

    global frame
    global window
    global skater_entry
    global program_entry
    global error_label

    skater = skater_entry.get()
    program_name = program_entry.get()

    if skater == '' or program_name == '':
        error_label.config(text="You must set Skater and Program information")
        error_label.pack(pady=5, padx=5)

    else:
        frame.destroy()

        program = Program(skater=skater, program_name=program_name)
        open_program(program)


# Display home
def home():

    global frame
    global window
    global skater_entry
    global program_entry
    global error_label

    # create frame
    frame = Frame(window, bg="#0a1526")
    title_frame = Frame(frame, bg="#0a1526")
    menu_frame = Frame(frame, bg="#0a1526")

    # create elements

    # title
    label_title = Label(title_frame, text="RollArt BV", font=("sans-serif", 24), bg="#0a1526", fg="white")
    label_title.pack()

    label_subtitle = Label(title_frame, text="Calculate your program base value in real time !", font=("sans-serif", 14), bg="#0a1526", fg="white")
    label_subtitle.pack()

    # menu
    error_frame = Frame(menu_frame, bg="red")
    error_label = Label(error_frame, text="", font=("sans-serif", 10), bg="red", fg="white", height=0)
    error_frame.pack()

    # Skater informations
    form_frame = Frame(menu_frame, bg="#0a1526")
    skater_label = Label(form_frame, text="Skater", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
    skater_label.grid(row=0, column=0, sticky="nw")
    skater_entry = Entry(form_frame, font=('sans-serif', 10), borderwidth=1, relief='flat')
    skater_entry.grid(row=1, column=0, sticky="nesw", ipadx=5, ipady=5)

    program_label = Label(form_frame, text="Program", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white")
    program_label.grid(row=0, column=1, sticky="nw")
    program_entry = Entry(form_frame, font=('sans-serif', 10), borderwidth=1, relief='flat')
    program_entry.grid(row=1, column=1, sticky="nesw", ipadx=5, ipady=5)

    form_frame.pack(pady=5, expand=YES)

    start_btn = Button(menu_frame, text="Start", font=("sans-serif", 14, "bold"), bg="#bd3800", fg="white", pady=8, command=start)
    start_btn.pack(pady=5, fill=X)

    config_btn = Button(menu_frame, text="Elements database", font=("sans-serif", 12), bg="#dfe7e8", command=elements_database.open_window)
    config_btn.pack(pady=5, fill=X)

    # add to window
    title_frame.pack(pady=15)
    menu_frame.pack(pady=15, fill=X)
    frame.pack(expand=YES)

# program window
def open_program(program):

    global frame
    global window

    #Grid.columnconfigure(window, 0, weight=1)
    #Grid.rowconfigure(window, 0, weight=1)

    # create frame
    frame = Frame(window, bg="#0a1526")

    #Grid.columnconfigure(frame, 0, weight=1)
    #Grid.rowconfigure(frame, 0, weight=1)

    title_frame = Frame(frame, bg="#bd3800")

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

    program_element_form()

    frame.pack(fill=X)

# element component
def program_element_form():

    global frame
    global element_i

    # create frame
    element_frame = Frame(frame, bg="#0a1526")

    Grid.rowconfigure(element_frame, 0, weight=1)

    label_item = Label(element_frame, text="#"+str(element_i), font=("sans-serif", 14), bg="#bd3800", fg="white", padx=10, width=3)
    label_item.grid(row=0, column=0, sticky="nsew");

    Grid.columnconfigure(element_frame, 1, weight=1)

    element_frame_items = Frame(element_frame, bg="#0a1526")

    element_frame_types = Frame(element_frame_items, bg="#0a1526")

    Grid.rowconfigure(element_frame_types, 0, weight=1)

    # list elements types
    btnLabels = ['SoloJump', 'ComboJump', 'SoloSpin', 'ComboSpin', 'Step', 'Choreo']
    btns = []
    i = 0

    for btnLabel in btnLabels:

        Grid.columnconfigure(element_frame_types, i, weight=1)

        btns.append(Button(element_frame_types, text=btnLabel, font=("sans-serif", 11), bg="#dfe7e8"))
        btns[i].grid(row=0, column=i, sticky="nsew")
        i += 1

    element_frame_types.pack(fill=X)

    element_frame_items.grid(row=0, column=1, sticky="nsew");

    element_frame.pack(pady=5, fill=X)

    element_i += 1

home()

# display window
window.mainloop()
