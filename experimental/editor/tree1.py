import tkinter.ttk as ttk
from tkinter import *
import os

class Tree(tk.Frame):

    def __init__(self, root, path):
        tk.Frame.__init__(self, root)
        self.root = root
        self.path = path
        self.initUI(self.path)

    def initUI(self, path):
        self.tree = ttk.Treeview(self.root)
        self.tree.bind("Double-Button-1>", self.itemEvent)
        yScr = ttk.Scrollbar(self.tree, orient = "vertical", command = self.tree.yview)
        xScr = ttk.Scrollbar(self.tree, orient = "horizontal", command = self.tree.xview)
        # self.tree.configure(yscroll = yScr.set, xScroll = xScr.set)
        self.tree.heading("#0", text = "My Tree", anchor = 'w')
        yScr.pack(side = RIGHT, fill = Y)

        pathy = os.path.abspath(path) 
        rootNode = self.tree.insert('', 'end', text = pathy, open = True)
        self.createTree(rootNode, pathy)

        self.tree.pack(side = LEFT, fill = BOTH, expand = 1, padx = 2, pady = 2)

        self.pack(fill= BOTH, expand = 1) 

    def createTree(self, parent, path):
        for p in os.listdir(path):
            pathy = os.path.join(path, p)
            isdir = os.path.isdir(pathy)
            oid = self.tree.insert(parent, 'end', text = p, open = False)
            if isdir:
               self.createTree(oid, pathy)

    def itemEvent(self, event):
        item = self.tree.selection()[0] # now you got the item on that tree
        print("you clicked on", self.tree.item(item,"text"))


def main():
    root = Tk()
    app = Tree(root)
    root.mainloop()


if __name__ == '__main__':
    main()
