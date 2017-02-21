from tkinter import *


class ResizingCanvas(Canvas):
    """
    Class for making dynamic resizing for the text window we are using.

    Example usage:
        root = Tk()
        txt_panel = Text(root)
        txt_panel.pack(fill=BOTH, expand=YES)
        ResizingCanvas(txt_panel, width=850, height=400,
                       bg="red", highlightthickness=0)

        root.mainloop()
    """
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
