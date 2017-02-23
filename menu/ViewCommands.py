from tkinter import *


class ViewCommands(Text):
    def __init__(self, root, canvas, **kwargs):
        """
        Class for all the edit commands of the text editor.
        """
        Text.__init__(self, root, **kwargs)
        self.canvas = canvas
        self.bind('<Control-Key-1>', self.zoom_in)
        self.bind('<Control-Key-2>', self.zoom_out)

    def zoom_in(self):
        self.canvas.zoom_in_scale()

    def zoom_out(self):
        self.canvas.zoom_out_scale()
