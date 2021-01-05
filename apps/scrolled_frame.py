
#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a forked version of a program developed by Eugene Bakin : 
# Github profile : https://github.com/bakineugene

# Original source code :
# https://gist.github.com/bakineugene/76c8f9bcec5b390e45df

# Improvements made by other contributors :
# - JackTheEngineer : https://github.com/JackTheEngineer (mousescroll system)
# - Guillaume MODARD : https://github.com/Guillaume35 (configurable widget and multi OS)

from tkinter import *
import platform
import functools
fp = functools.partial

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        # The following code manage mousewheel system depending on OS used
        def _on_mousewheel(event, scroll = None):
            if  platform.system() == 'Linux':
                self.canvas.yview_scroll(int(scroll), "units")

            elif platform.system() == 'Windows':
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_to_mousewheel(event):
            if  platform.system() == 'Linux':
                self.canvas.bind_all("<Button-4>", fp(_on_mousewheel, scroll=-1))
                self.canvas.bind_all("<Button-5>", fp(_on_mousewheel, scroll=1))
            
            elif platform.system() == 'Windows':
                self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            if  platform.system() == 'Linux':
                self.canvas.unbind_all("<Button-4>")
                self.canvas.unbind_all("<Button-5>")

            elif platform.system() == 'Windows':
                self.canvas.unbind_all("<MouseWheel>")

        self.canvas.bind('<Configure>', _configure_canvas)
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            self.root = Tk()


            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)

            self.frame = VerticalScrolledFrame(self.root)
            self.frame.grid(row=0, column=0, sticky="nsew")
            self.label = Label(text="Shrink the window to activate the scrollbar.")
            self.label.grid(row=1, column=0, sticky="nsew")
            buttons = []
            for i in range(10):
                buttons.append(Button(self.frame.interior, text="Button " + str(i)))
                buttons[-1].pack(fill=X)

    app = SampleApp()
    app.root.mainloop()