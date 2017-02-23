from tkinter import *


class ViewCommands(Text):
    def __init__(self, root, text_editor, **kwargs):
        """
        Class for all the edit commands of the text editor.
        """
        Text.__init__(self, root, **kwargs)
        self.text_editor = text_editor
        # self.bind('<Control->', self.zoom_in)
        # self.bind('<Control->', self.zoom_out)
        self.size = 16

    def zoom_in(self):
        self.size += 1
        self.text_editor.font.configure(size=self.size)

    def zoom_out(self):
        print('Zoom out to {}'.format(self.size))
        self.size -= 1
        self.text_editor.font.configure(size=self.size)
