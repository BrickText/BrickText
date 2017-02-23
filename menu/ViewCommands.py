from tkinter import *
from settings.SettingsVariables import settings


class ViewCommands(Text):
    def __init__(self, root, lines, text_editor, **kwargs):
        """
        Class for all the edit commands of the text editor.
        """
        Text.__init__(self, root, **kwargs)
        self.text_editor = text_editor
        self.lines = lines
        # self.bind('<Control->', self.zoom_in)
        # self.bind('<Control->', self.zoom_out)

    def zoom_in(self):
        settings['letter_size'] += 2
        self.text_editor.font.configure(size=settings['letter_size'])
        self.lines.step = settings['letter_size']

    def zoom_out(self):
        settings['letter_size'] -= 1
        self.text_editor.font.configure(size=settings['letter_size'])
        self.lines.step = settings['letter_size']
