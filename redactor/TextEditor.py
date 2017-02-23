from tkinter import *
from tkinter import font


class TextEditor():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BrickText")
        self.text_panel = Text(self.root)
        self.text_panel.pack(side=RIGHT, fill=BOTH, expand=YES)
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
