from tkinter import *
from motor.element import *
from os import listdir
from os.path import isfile, join
from pathlib import Path
import re
from functools import partial

labels = [
    {
        'var': 'name',
        'label': 'Name',
        'width': 15,
        'font': 'sans-serif'
    },
    {
        'var': 'code',
        'label': 'Code',
        'width': 10,
        'font': 'sans-serif'
    },
    {
        'var': 'qoe3',
        'label': '+3'
    },
    {
        'var': 'qoe2',
        'label': '+2'
    },
    {
        'var': 'qoe1',
        'label': '+1'
    },
    {
        'var': 'base',
        'label': 'BASE'
    },
    {
        'var': 'under',
        'label': '<'
    },
    {
        'var': 'half',
        'label': '<<'
    },
    {
        'var': 'down',
        'label': '<<<'
    },
    {
        'var': 'qoem1',
        'label': '-1'
    },
    {
        'var': 'qoem2',
        'label': '-2'
    },
    {
        'var': 'qoem3',
        'label': '-3'
    },
    {
        'var': 'base_combo',
        'label': 'COMBO'
    },
    {
        'var': 'combo_under',
        'label': 'Comb<'
    },
    {
        'var': 'combo_half',
        'label': 'Comb<<'
    },
    {
        'var': 'combo_down',
        'label': 'Comb<<<'
    }
]
entries = []
entries_i = 0
table_frame = None

def open_window():

    global labels
    global entries
    global entries_i
    global table_frame

    # Create main window
    window = Tk()

    # Customizing window
    window.title("Elements database - RollArt BV")
    window.geometry("1280x720")
    window.minsize(480,360)
    window.config(background="#0a1526")

    # create frame
    frame = Frame(window, bg="#0a1526")
    title_frame = Frame(frame, bg="#0a1526")
    table_frame = Frame(frame, bg="#0a1526")

    # create elements

    # title
    label_title = Label(title_frame, text="Elements database", font=("sans-serif", 14), bg="#0a1526", fg="white")
    label_title.pack()

    header = []

    # If not allready created
    entries = []
    entries.append([])

    for i in range(len(labels)):

        if 'width' in labels[i].keys():
            width = labels[i]['width']
        else:
            width = 8


        if 'font' in labels[i].keys():
            font = labels[i]['font']
        else:
            font = 'monospace'

        header.append(Label(table_frame, text=labels[i]['label'], font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white"))
        header[i].grid(row=0, column=i)

        entries[0].append(Entry(table_frame, width=width, font=(font, 10), borderwidth=1, relief='flat'))
        entries[0][i].grid(row=1, column=i, sticky="nesw")

    # New element form
    header.append(Label(table_frame, text="", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white"))
    header[i+1].grid(row=0, column=i+1)
    entries[0].append(Button(table_frame, text="Add", font=("sans-serif", 10), bg="#dfe7e8", command=lambda: record_element(0), borderwidth=1))
    entries[0][i+1].grid(row=1, column=i+1, sticky="nesw")

    # List existing elements
    home_path = str(Path.home())
    elements_dir = home_path + '/.rollartBV/elements'
    data_files = [f for f in listdir(elements_dir) if isfile(join(elements_dir, f))]

    entries_i = 1

    for file_name in data_files:
        if re.match(r'^\w+\.json$', file_name):
            code = file_name.replace('.json', '')
            element = Element(code)
            add_entry(element)


    # add to window
    title_frame.pack(pady=15)
    table_frame.pack(pady=15)
    frame.pack(fill=X)

    # display window
    window.mainloop()

# add editable entry on table
def add_entry(element):

    global entries
    global entries_i
    global table_frame
    global labels

    entries.append([])

    for j in range(len(labels)):

        if 'width' in labels[j].keys():
            width = labels[j]['width']
        else:
            width = 8

        if 'font' in labels[j].keys():
            font = labels[j]['font']
        else:
            font = 'monospace'

        data = element.getAll()

        entries[entries_i].append(Entry(table_frame, width=width, font=(font, 10), borderwidth=1, relief='flat'))
        entries[entries_i][j].insert(0, data[labels[j]['var']])
        entries[entries_i][j].grid(row=entries_i+1, column=j, sticky="nesw")

    action = partial(record_element, entries_i)
    entries[entries_i].append(Button(table_frame, text="Save", font=("sans-serif", 10), bg="#dfe7e8", command=action, borderwidth=1))
    entries[entries_i][j+1].grid(row=entries_i+1, column=j+1, sticky="nesw")

    entries_i += 1

# record a new element
def record_element(row):

    global labels
    global entries

    data = {}

    for i in range(len(labels)):
        data[labels[i]['var']] = entries[row][i].get()

        if (row == 0):
            entries[row][i].delete(0, END)

    # Create and record elements with values
    element = Element(data)
    element.record()

    if (row == 0):
        add_entry(element)

if __name__ == '__main__':
    open_window()
