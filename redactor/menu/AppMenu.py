from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfile
from tkinter.colorchooser import *
import json
import os

from redactor.menu.EditCommands import EditCommands
from redactor.menu.ViewCommands import ViewCommands
from redactor.settings.LanguageSettings import languages
from redactor.settings.SettingsVariables import settings


class AppMenu(Frame):
    """
    Class which creates menubar for any type of frame.
    It will create the following menus with the following featues:
    File -> Open(opens file), Save(Saves current file), Save as(Same as Save)
    Edit -> Cut, Copy, Paste
    """

    def __init__(self, root, text_panel, color, text, lines, tree):
        Frame.__init__(self, root)
        self.root = root
        self.text_panel = text_panel
        self.color = color
        self.text = text
        self.lines = lines
        self.tree = tree
        self.number_of_windows = 0
        self.new_keywords = {}
        self.color_keyword = None
        self.keyword = None
        self.string = False
        self.function = False

        self.menubar = Menu(root)
        self.gen_filemenu()
        self.gen_editmenu()
        self.gen_viewmenu()
        self.gen_preferencesmenu()

        root.config(menu=self.menubar)

    # Add tab for filemenu menu
    def gen_filemenu(self):
        filemenu = Menu(self.menubar, tearoff=0)

        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open)
        filemenu.add_separator()

        filemenu.add_command(label="Save as", command=self.save_as)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.exit)

        self.menubar.add_cascade(label="File", menu=filemenu)
        self.root.bind("<Control-n>", lambda _: self.new_file())
        self.root.bind("<Control-s>", lambda _: self.save())
        self.root.bind("<Control-o>", lambda _: self.open())
        self.root.bind("<Control-q>", lambda _: self.exit())

    def new_file(self):
        self.save()
        self.text_panel.delete(1.0, "end")
        self.text.set_filename("untitled")


    # Add tab for edit menu
    def gen_editmenu(self):
        functionality = EditCommands(self.root, self.text_panel)
        editmenu = Menu(self.menubar, tearoff=0)

        editmenu.add_command(label='Cut', command=functionality.cut)
        editmenu.add_command(label='Copy', command=functionality.copy)
        editmenu.add_command(label='Paste', command=functionality.paste)

        self.menubar.add_cascade(label="Edit", menu=editmenu)

    # Add tab for view menu
    def gen_viewmenu(self):
        functionality = ViewCommands(self.root, self.text, self.lines)
        viewmenu = Menu(self.menubar, tearoff=0)

        viewmenu.add_command(label='Zoom in', command=functionality.zoom_in)
        viewmenu.add_command(label='Zoom out', command=functionality.zoom_out)

        self.menubar.add_cascade(label='View', menu=viewmenu)

    # Add tab for preferences menu
    def gen_preferencesmenu(self):
        preferencesmenu = Menu(self.menubar, tearoff=0)

        preferencesmenu.add_command(label="Language preferences",
                                    command=self.language_preferences)
        preferencesmenu.add_command(label="Common words preferences",
                                    command=self.common_words_preferences)
        preferencesmenu.add_command(label="Editor preferences",
                                    command=self.editor_preferences)

        self.menubar.add_cascade(label="Preferences", menu=preferencesmenu)

    # Opens file
    def open(self):
        file = askopenfile(parent=self.root, mode='rb',
                           title='Select a file')
        if file is not None:
            self.text.set_filename(file.name)
            contents = file.read()
            self.text_panel.delete('1.0', END)
            self.text_panel.insert('1.0', contents)
            self.color.reset_tags(languages[self.get_file_language()])
            file.close()

    # Saves current file
    def save(self):
        if not self.text.get_filename():
            print('calling save as')
            self.save_as()
        else:
            file_text = self.text_panel.get("1.0", END)
            with open(self.text.get_filename(), 'w') as f:
                f.write(file_text)

    # Saves current file as another one
    def save_as(self):
        filename = asksaveasfilename()
        if filename:
            full_text = self.text_panel.get("1.0", END)
            with open(filename, 'w') as f:
                f.write(full_text)
        self.text.set_filename(filename)

    def exit(self):
        self.root.destroy()

    # Get language of current file
    def get_file_language(self):
        return self.text.get_filename().split('.')[-1]\
               if self.text.get_filename() else False

    # Add window for language preferences
    def language_preferences(self):
        self.number_of_windows += 1

        self.t = Toplevel(self)
        self.t.wm_title('Language preferences')

        l = Label(self.t, text='Keyword')
        l.pack(side='top', padx=10, pady=10)

        self.e = Entry(self.t)
        self.e.pack(side='top')

        b = Button(self.t, text='Select Color', command=self.getColor)
        b.pack(side='top', padx=10, pady=10)

    # Add window for language preferences
    def editor_preferences(self):
        self.number_of_windows += 1
        self.t = Toplevel(self)
        self.t.wm_title('Editor preferences')

        l = Label(self.t, text='Size')
        l.pack(side='top', padx=10, pady=10)
        e = Entry(self.t)
        e.pack(side='top')
        b = Button(self.t, text='Ok',
                   command=lambda: self.get_size(e.get()))
        b.pack(side='top', padx=10, pady=10)

        l = Label(self.t, text='Editor background_color')
        l.pack(side='top', padx=10, pady=10)
        b = Button(self.t, text='Select Color', command=self.getColor)
        b.pack(side='top', padx=10, pady=10)

        l = Label(self.t, text='Tree background_color')
        l.pack(side='top', padx=10, pady=10)
        b = Button(self.t, text='Select Color',
                   command=lambda: self.getColor(tree='tree_background_color'))
        b.pack(side='top', padx=10, pady=10)

        l = Label(self.t, text='Tree frame color')
        l.pack(side='top', padx=10, pady=10)
        b = Button(self.t, text='Select Color',
                   command=lambda: self.getColor(tree='tree_frame_color'))
        b.pack(side='top', padx=10, pady=10)

        l = Label(self.t, text='Tree letter color')
        l.pack(side='top', padx=10, pady=10)
        b = Button(self.t, text='Select Color',
                   command=lambda: self.getColor(tree='tree_letter_color'))
        b.pack(side='top', padx=10, pady=10)

        self.e = None

    def common_words_preferences(self):
        self.number_of_windows += 1

        self.t = Toplevel(self)
        self.t.wm_title('Common words preferences')

        l = Label(self.t, text='String')
        l.pack(side='top', padx=10, pady=10)

        b = Button(self.t, text='Select Color',
                   command=lambda: self.getColor(string=True))
        b.pack(side='top', padx=10, pady=10)

        l = Label(self.t, text='Function')
        l.pack(side='top', padx=10, pady=10)

        b = Button(self.t, text='Select Color',
                   command=lambda: self.getColor(function=True))
        b.pack(side='top', padx=10, pady=10)

        self.e = None

    # Get input for color
    def getColor(self, string=False, function=False, tree=None):
        self.color_keyword = askcolor()[1]

        if self.color_keyword:
            if self.e:
                self.keyword = self.e.get()
            elif string:
                self.string = True
            elif function:
                self.function = True
            else:

                with open(os.path.dirname(__file__) +
                          '/../settings/redactor_settings.json') as data_file:
                    rs = eval(data_file.read())

                if tree:
                    rs[tree] = self.color_keyword
                else:
                    rs['background_color'] = self.color_keyword

                with open(os.path.dirname(__file__) +
                          '/../settings/redactor_settings.json', 'w') as data_file:
                    data_file.write(json.dumps(rs))

                if tree:
                    self.tree.set_background_color()
                else:
                    self.text_panel.configure(background=self.color_keyword)

    # Get input for size
    def get_size(self, size):
        settings['letter_size'] = int(size)
        self.text.font.configure(size=settings['letter_size'])
        self.lines.font.configure(size=settings["letter_size"])
        self.lines.step = settings['letter_size']

    def close(self):
        self.t.destroy()
