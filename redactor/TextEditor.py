from tkinter import *
from tkinter import font


class TextEditor():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BrickText")
        self.font = font.Font(size=16)
        self.text_panel = Text(self.root, font=self.font)
        self.text_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

    def start(self):
        self.root.mainloop()

    def get_root(self):
        return self.root

    def get_text_panel(self):
        return self.text_panel
