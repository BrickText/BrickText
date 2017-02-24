from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfile
from tkinter.colorchooser import *

from menu.EditCommands import EditCommands
from menu.ViewCommands import ViewCommands
from settings.LanguageSettings import languages


class AppMenu(Frame):
    """
    Class which creates menubar for any type of frame.
    It will create the following menus with the following featues:
    File -> Open(opens file), Save(Saves current file), Save as(Same as Save)
    Edit -> Cut, Copy, Paste
    """

    def __init__(self, root, text_panel, text, lines):
        Frame.__init__(self, root)
        self.root = root
        self.text_panel = text_panel
        self.text = text
        self.lines = lines
        self.number_of_windows = 0
        self.new_keywords = {}

        self.menubar = Menu(root)
        self.gen_filemenu()
        self.gen_editmenu()
        self.gen_viewmenu()
        self.gen_preferencesmenu()

        self.filename = ''
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

    def gen_editmenu(self):
        functionality = EditCommands(self.root, self.text_panel)
        editmenu = Menu(self.menubar, tearoff=0)

        editmenu.add_command(label='Cut', command=functionality.cut)
        editmenu.add_command(label='Copy', command=functionality.copy)
        editmenu.add_command(label='Paste', command=functionality.paste)

        self.menubar.add_cascade(label="Edit", menu=editmenu)

    def gen_viewmenu(self):
        functionality = ViewCommands(self.root, self.text, self.lines)
        viewmenu = Menu(self.menubar, tearoff=0)

        viewmenu.add_command(label='Zoom in', command=functionality.zoom_in)
        viewmenu.add_command(label='Zoom out', command=functionality.zoom_out)

        self.menubar.add_cascade(label='View', menu=viewmenu)

    def gen_preferencesmenu(self):
        preferencesmenu = Menu(self.menubar, tearoff=0)

        preferencesmenu.add_command(label="Language preferences",
                                    command=self.language_preferences)
        # preferencesmenu.add_command(label="Editor preferences",
        #                             command=self.editor_preferences)

        self.menubar.add_cascade(label="Preferences", menu=preferencesmenu)

    # Opens file
    def open(self):
        file = askopenfile(parent=self.root, mode='rb',
                           title='Select a file')
        self.filename = file.name
        if file is not None:
            contents = file.read()
            self.text_panel.delete('1.0', END)
            self.text_panel.insert('1.0', contents)
            file.close()

    # Saves current file
    def save(self):
        if not self.filename:
            print('calling save as')
            self.save_as()
        else:
            file_text = self.text_panel.get("1.0", END)
            with open(self.filename, 'w') as f:
                f.write(file_text)

    # Saves current file as another one
    def save_as(self):
        filename = asksaveasfilename()
        if filename:
            full_text = self.text_panel.get("1.0", END)
            with open(filename, 'w') as f:
                f.write(full_text)
        self.filename = filename

    def exit(self):
        self.root.destroy()

    def get_file_language(self):
        return self.filename.split('.')[1] if self.filename else False

    def language_preferences(self):
        self.number_of_windows += 1
        self.t = Toplevel(self)
        self.t.wm_title('Language preferences')
        with open('settings/{}_keywords.json'
                  .format(languages[self.get_file_language()])) as data_file:
            keywords = eval(data_file.read())
        for k, _ in keywords.items():
            l = Label(self.t, text=k)
            l.pack(side='top', padx=10, pady=10)
            b = Button(self.t, text='Select Color', command=self.getColor)
            b.pack(side='top', padx=10, pady=10)
        b = Button(self.t, text='Ok', command=self.close)
        b.pack()

    def editor_preferences(self):
        print("editor")

    def getColor(self, keyword):
        color = askcolor()
        print(color)

    def close(self):
        self.t.destroy()
