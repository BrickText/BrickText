import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

from redactor.settings.LanguageSettings import languages


class Tree(tk.Frame):
    """
    This class is for set tree
    """

    def __init__(self, editor, root, path, color):
        self.editor = editor
        self.root = root
        self.color = color
        tk.Frame.__init__(self, root)
        self.tree = ttk.Treeview(self)
        self.tree.bind("<Double-Button-1>", self.itemEvent)
        ysb = ttk.Scrollbar(self, orient='vertical',
                            command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal',
                            command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=path, anchor='w')
        self.tree.column("#0", minwidth=250, width=250, stretch=NO)

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)

        ysb.pack(side=RIGHT, fill=Y)
        xsb.pack(side=BOTTOM, fill=X)
        self.pack(side=LEFT, fill=BOTH, expand=FALSE, padx=2, pady=2)
        self.tree.pack(side=LEFT, fill=BOTH, expand=FALSE, padx=2, pady=2)

    # Get file tree
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

    # Open file from tree
    def itemEvent(self, event):
        item = self.tree.selection()[0]
        path = self.get_path(item)
        if os.path.isfile(path):
            self.editor.set_filename(path)
            with open(path, 'r') as file:
                contents = file.read()
                self.editor.get_text_panel().delete('1.0', END)
                self.editor.get_text_panel().insert('1.0', contents)
                self.color.reset_tags(languages[self.editor.
                                                get_file_language()])

    # Get path of file in tree
    def get_path(self, item):
        item_path = [item]
        path = ''
        while item != '':
            item = self.tree.parent(item)
            if item != '':
                item_path.append(item)
        for el in item_path[::-1]:
            part = self.tree.item(el, 'text')
            if part[0] != '/':
                part = '/' + part
            path += part
        return path
