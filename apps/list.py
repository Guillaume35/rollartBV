from tkinter import *
from functools import partial

class ListApp:

    def __init__(self, window, className, title="List", data=[], labels=[], actions=[], default={}):

        self.frame = Frame(window, bg="#0a1526")
        self.title_frame = Frame(self.frame, bg="#0a1526")
        self.table_frame = Frame(self.frame, bg="#0a1526")
        self.data = data
        self.labels = labels
        self.actions = actions
        self.title = title
        self.entries = []
        self.header = []
        self.default_font = 'monospace'
        self.default_width = 7
        self.className = className
        self.default = default

    def add_row(self, data):

        i = len(self.entries)
        self.entries.append([])

        for j in range(len(self.labels)):

            if 'width' in self.labels[j].keys():
                width = self.labels[j]['width']
            else:
                width = self.default_width

            if 'font' in self.labels[j].keys():
                font = self.labels[j]['font']
            else:
                font = self.default_font

            value = data[self.labels[j]['var']]

            if not value and value != 0:
                value = ''

            self.entries[i].append(Entry(self.table_frame, width=width, font=(font, 10), borderwidth=1, relief='flat'))
            self.entries[i][j].insert(0, value)
            self.entries[i][j].grid(row=i+1, column=j, sticky="nesw")

        action = partial(self.record, i, data)
        self.entries[i].append(Button(self.table_frame, text="Save", font=("sans-serif", 10), bg="#dfe7e8", command=action, borderwidth=1))
        self.entries[i][j+1].grid(row=i+1, column=j+1, sticky="nesw")

        for a in range(len(self.actions)):

            actionData = self.actions[a]

            if 'params' in actionData:
                action = partial(actionData['action'], data, actionData['params'])
            
            else:
                action = partial(actionData['action'], data)

            self.entries[i].append(Button(self.table_frame, text=actionData['label'], font=("sans-serif", 10), bg="#dfe7e8", command=action, borderwidth=1))
            self.entries[i][j+a+2].grid(row=i+1, column=j+a+2, sticky="nesw")


    def record(self, row, data):

        for i in range(len(self.labels)):
            data[self.labels[i]['var']] = self.entries[row][i].get()

            if (row == 0):
                self.entries[row][i].delete(0, END)

        for key, val in self.default.items():
            if not key in data:
                data[key] = val

        ob = self.className(data)
        ob.record()

        if (row == 0):
            self.add_row(data)

    def display(self):

        # create elements

        # title
        label_title = Label(self.title_frame, text=self.title, font=("sans-serif", 14), bg="#0a1526", fg="white")
        label_title.pack()

        # create header and new item row
        self.entries.append([])

        for i in range(len(self.labels)):

            if 'width' in self.labels[i].keys():
                width = self.labels[i]['width']
            else:
                width = self.default_width

            if 'font' in self.labels[i].keys():
                font = self.labels[i]['font']
            else:
                font = self.default_font

            Grid.columnconfigure(self.table_frame, i, weight=1)

            self.header.append(Label(self.table_frame, text=self.labels[i]['label'], font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white",  borderwidth=1, relief="groove"))
            self.header[i].grid(row=0, column=i, sticky="nesw")

            self.entries[0].append(Entry(self.table_frame, width=width, font=(font, 10), borderwidth=1, relief='flat'))

            if 'value' in self.labels[i].keys():
                self.entries[0][i].insert(END, self.labels[i]['value'])
            
            self.entries[0][i].grid(row=1, column=i, sticky="nesw")


        # New element form
        self.header.append(Label(self.table_frame, text="", font=("sans-serif", 10, "bold"), bg="#0a1526", fg="white"))
        self.header[i+1].grid(row=0, column=i+1)
        action = partial(self.record, 0, {})
        self.entries[0].append(Button(self.table_frame, text="Add", width=5, font=("sans-serif", 10), command=action, bg="#dfe7e8", borderwidth=1))
        self.entries[0][i+1].grid(row=1, column=i+1, sticky="nesw")

        for d in self.data:
            self.add_row(d)

        # add to window
        self.title_frame.pack(pady=15)
        self.table_frame.pack(pady=15, fill=X)
        self.frame.pack(fill=X)
