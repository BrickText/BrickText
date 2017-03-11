from tkinter import *
import re
import ast


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

    def __init__(self, text_panel, root, **kwargs):
        Canvas.__init__(self, text_panel, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.root = root
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, 1.1, 1.1)


class AutocompleteEntry(Text):
    def __init__(self, *args, **kwargs):

        Text.__init__(self, *args, **kwargs)
        self.lista = ''
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)  # Binds Writing to self.changed
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get().split(' ')[-1] == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(),
                                  y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            already_written = ''
            for ind in range(len(self.var.get().split(' ')) - 1):
                already_written += self.var.get().split(' ')[ind] + ' '
            print(already_written)
            self.var.set(already_written + self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            # Change Cursor place

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        try:
            text = ast.parse(self.var.get())
            self.lista = set()
            for node in ast.walk(text):
                if isinstance(node, ast.FunctionDef):
                    self.lista.add(node.name)
                if isinstance(node, ast.Name):
                    self.lista.add(node.id)
        except Exception:
            print('Highlight the line for bad syntax')
        print(self.lista)
        pattern = re.compile('.*' + self.var.get().split(' ')[-1] + '.*')
        return [w for w in self.lista if re.match(pattern, w)]


if __name__ == '__main__':
    root = Tk()

    text = AutocompleteEntry(root)
    text.grid(row=0, column=0)
    ResizingCanvas(text, root, width=500, height=300)
    text.pack()
    # entry.pack()
    print(isinstance(text, Text))
    # Button(text='nothing').grid(row=1, column=0)
    # Button(text='nothing').grid(row=2, column=0)
    # Button(text='nothing').grid(row=3, column=0)

    root.mainloop()
