from tkinter import *
import re
import ast


class AutocompleteText(Text):

    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.lista = set()
        self.bind("<Control-space>", self.called_autocomplete)
        self.lb_on = False

    def called_autocomplete(self, event):
        requested_word = self.get('1.0', END).strip().split()[-1]
        self.take_lista()
        self.generate_listbox(self.suitable_words(requested_word))

    def generate_listbox(self, words):
        if not self.lb_on:
            self.lb = Listbox()
            self.lb.bind("<Tab>", self.selection)
            self.lb.bind("<Up>", self.move_in_lb)
            self.lb.bind("<Down>", self.move_in_lb)
            self.lb_on = True
            self.lb.place(x=self.winfo_x(),
                          y=self.winfo_y() + self.winfo_height())
            for word in words:
                self.lb.insert(END, word)
            self.lb.pack()

    def move_in_lb(self, event):
        move_dir = -1 if event.keycode == '116' else 1
        if self.lb_on:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) + move_dir)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def selection(self, event):
        if self.lb_on:
            start_pos = self.index(INSERT)
            while(True):
                start_ind2 = start_pos.split('.')[1]
                start_ind2 = str(int(start_ind2) - 1)
                start_pos = start_pos.split('.')[0] + '.' + start_ind2
                if start_ind2 == '0' or\
                        not re.match(r"\s", self.get(start_pos)):
                    break
            self.delete(start_pos, INSERT)
            self.insert(INSERT, self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_on = False

    def suitable_words(self, requested_word):
        pattern = re.compile('.*' + requested_word + '.*')
        return [word for word in self.lista if re.match(pattern, word)]

    def take_lista(self):
        written_code = ast.parse(self.get('1.0', END).strip())
        self.lista = set()
        try:
            for node in ast.walk(written_code):
                if isinstance(node, ast.FunctionDef):
                    self.lista.add(node.name)
                if isinstance(node, ast.Name):
                    self.lista.add(node.id)
        except:
            print('Highlight line for bad syntax')

def main():
    root = Tk()

    text = AutocompleteText(root)
    text.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
