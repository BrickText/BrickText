from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfile


class AppMenu(Frame):
    """
    Class which creates menubar for any type of frame.
    It will create the following menus with the following featues:
    File -> Open(opens file), Save(Saves current file), Save as(Same as Save)
    """
    def __init__(self, root, text_panel):
        Frame.__init__(self, root)
        self.root = root
        self.menubar = Menu(root)
        self.gen_filemenu()
        self.text_panel = text_panel
        root.config(menu=self.menubar)

    def gen_filemenu(self):
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open)
        filemenu.add_separator()

        filemenu.add_command(label="Save as", command=self.save_as)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=filemenu)

    # Opens file
    def open(self):
        # askopenfile return opened file however can't access it
        with askopenfile(mode='w+') as f:
            for line in f:
                print(line)

    # Saves current file
    def save(self):
        pass

    # Saves current file as another one
    def save_as(self):
        filename = asksaveasfilename()
        if filename:
            full_text = self.text_panel.get("1.0", END)
            with open(filename, 'w') as f:
                f.write(full_text)

    def exit(self):
        self.root.destroy()
