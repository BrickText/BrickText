import os
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import *


class Tree(tk.Frame):
    def __init__(self, root, path):
        tk.Frame.__init__(self, root)
        self.tree = ttk.Treeview(root)
        self.tree.bind("<Double-Button-1>", self.itemEvent)
        ysb = ttk.Scrollbar(self.tree, orient='vertical',
                            command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree, orient='horizontal',
                            command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=path, anchor='w')
        # self.tree.column("#0", minwidth=0, width=300, stretch=NO)

        ysb.pack(side=RIGHT, fill=Y)

        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)

        self.tree.pack(side=LEFT, fill=BOTH, expand=1, padx=2, pady=2)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

    def itemEvent(self, event):
        item = self.tree.selection()[0]
        path = self.get_path(item)
        if os.path.isfile(path):
            pass

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
