from tkinter import *


class EditCommands(Text):
    def __init__(self, root, text_panel, **kwargs):
        """
        Class for all the edit commands of the text editor.
        """
        Text.__init__(self, root, **kwargs)
        self.text_panel = text_panel
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-p>', self.paste)

    def copy(self):
        text = self.text_panel.get(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)

    def cut(self):
        text = self.text_panel.get(SEL_FIRST, SEL_LAST)
        self.text_panel.delete(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)

    def paste(self):
        try:
            text = self.text_panel.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except:
            pass
