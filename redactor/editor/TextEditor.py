from tkinter import *
from tkinter import font
import os

from redactor.settings.SettingsVariables import settings
from redactor.autocomplete.AutoCompleteText import AutocompleteText


class TextEditor():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BrickText")
        self.font = font.Font(size=settings["letter_size"])
        self.text_panel = AutocompleteText(self.root, font=self.font)
        self.text_panel.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.filename = ''
        self.set_background_color()
        self.set_tabs()

    # Start editor
    def start(self):
        self.root.mainloop()

    def get_root(self):
        return self.root

    def get_text_panel(self):
        return self.text_panel

    def get_filename(self):
        return self.filename

    def get_file_language(self):
        return self.filename.split('.')[1] if self.filename else False

    def set_filename(self, filename):
        self.filename = filename

    # Set tab size
    def set_tabs(self):
        f = font.Font(font=self.text_panel['font'])
        tab_width = f.measure(' ' * 4)
        self.text_panel.config(tabs=(tab_width,))

    # Set background color
    def set_background_color(self):
        with open(os.path.dirname(__file__) +
                  '/../settings/redactor_settings.json') as rs:
            bg = eval(rs.read())['background_color']
        self.text_panel.configure(background=bg)
