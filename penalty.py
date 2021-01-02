import sqlite3
from tkinter import *
from tkinter import messagebox
import tools

class PenaltyApp:

    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.entry = None

    def confirm(self):
        val = float(self.entry.get())

        if val <= 0:
            self.parent.program.penalization = val
            self.parent.program.record()
            self.parent.program_score()
            self.window.destroy()

        else:
            messagebox.showwarning(title="Penalty alert", message="Only <= 0 value accepted", parent=self.window)

    def open_window(self):

        # Create main window
        self.window = Tk()

        # Customizing window
        self.window.title("Penalty - RollArt BV")
        self.window.geometry("500x300")
        self.window.minsize(480,360)
        self.window.config(background="#0a1526")

        frame = Frame(self.window, bg="")

        label = Label(frame, text="Penalty", font=("sans-serif", 14), bg="#0a1526", fg="white")
        label.pack(fill=X, pady=10)

        self.entry = Entry(frame, font=('sans-serif', 14), borderwidth=1, relief='flat')
        self.entry.insert(END, self.parent.program.penalization)
        self.entry.pack(fill=X, pady=10)

        btn = Button(frame, font=('sans-serif', 14, 'bold'), text="Confirm", bg="green", fg="white", pady=10, command=self.confirm)
        btn.pack(fill=X, pady=10)

        frame.pack(fill=X)

        # display window
        self.window.mainloop()
