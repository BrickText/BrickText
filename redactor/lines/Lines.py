from tkinter import *

from redactor.settings.SettingsVariables import settings


class Lines:
    """
    This class is for setting line numbers
    """

    def __init__(self, root, text_panel):
        self.root = root
        self.text_panel = text_panel
        self.font = font.Font(size=settings['letter_size'])
        self.lnText = Text(self.root,
                           width=4,
                           padx=4,
                           highlightthickness=0,
                           takefocus=0,
                           bd=0,
                           background='lightgrey',
                           foreground='magenta',
                           state='disabled',
                           font=self.font)
        self.lnText.pack(side=LEFT, fill='y')
        self.lineNumbers = ''

    # Set line numbers
    def getLineNumbers(self):
        line = '0'
        col = ''
        ln = ''
        # assume each line is at least 6 pixels high
        self.step = settings['letter_size']
        nl = '\n'
        lineMask = '    %s\n'
        indexMask = '@0,%d'
        for i in range(0, self.text_panel.winfo_height(), self.step):
            ll, cc = self.text_panel.index(indexMask % i).split('.')
            if line == ll:
                if col != cc:
                    col = cc
                    ln += nl
            else:
                line, col = ll, cc
                ln += (lineMask % line)[-5:]
        return ln

    # Update line numbers
    def updateLineNumbers(self):
        tt = self.lnText
        ln = self.getLineNumbers()
        if self.lineNumbers != ln:
            self.lineNumbers = ln
            tt.config(state='normal')
            tt.delete('1.0', END)
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')

    def updateAllLineNumbers(self):
        self.updateLineNumbers()
