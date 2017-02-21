from tkinter import *


class TextEditor():
    def __init__(self):
        self.root = Tk()
        # screenName='BrickText'
        self.editor = Text(self.root)

    def start(self):
        self.editor.pack()
        self.root.mainloop()

    def get_root(self):
        return self.root
