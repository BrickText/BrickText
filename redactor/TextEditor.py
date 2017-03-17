from tkinter import *
from tkinter import font

from settings.SettingsVariables import settings
from redactor.AutoCompleteText import AutocompleteText


class TextEditor():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BrickText")
        self.font = font.Font(size=settings["letter_size"])
        self.text_panel = AutocompleteText(self.root, font=self.font)
        self.text_panel.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.set_background_color()
        self.set_tabs()

    def start(self):
        self.root.mainloop()

    def get_root(self):
        return self.root

    def get_text_panel(self):
        return self.text_panel

    def set_tabs(self):
        f = font.Font(font=self.text_panel['font'])
        tab_width = f.measure(' ' * 3)
        self.text_panel.config(tabs=(tab_width,))

    def set_background_color(self):
        with open('settings/redactor_settings.json') as rs:
            bg = eval(rs.read())['background_color']
        self.text_panel.configure(background=bg)
