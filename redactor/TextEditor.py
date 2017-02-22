from tkinter import *


class TextEditor():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BrickText")
        self.text_panel = Text(self.root)
        self.text_panel.pack(fill=BOTH, expand=YES)

    def start(self):
        self.root.mainloop()

    def get_root(self):
        return self.root
    
    def get_text_widget(self):
        return self.editor

    def get_text_panel(self):
        return self.text_panel
