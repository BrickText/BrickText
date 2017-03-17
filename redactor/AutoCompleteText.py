from tkinter import *
import re
import ast

from settings.SettingsVariables import settings

FONT_SIZE = settings["letter_size"]


class AutocompleteText(Text):
    """
        Text class which adds to your text widget AutoComplete ListBox
    """

    def __init__(self, root, *args, **kwargs):
        Text.__init__(self, root, *args, **kwargs)
        self.lista = set()
        self.root = root
        self.bind("<Control-space>", self.called_autocomplete)

    def called_autocomplete(self, event):
        requested_word = self.get(self.get_start_pos(), INSERT).strip()
        self.take_lista()
        self.suggestion_menu(self.suitable_words(requested_word))

    def suggestion_menu(self, words):
        self.sugg_menu = Menu(self.root)
        for w in words:
            self.sugg_menu.add_command(label=w,
                                       command=lambda w=w: self.insert_w(w))
            print("Label:", w)
        self.position_menu()

    def position_menu(self):
        row = self.index(INSERT)[0]
        print('Tabs LEngth -', len(self.get(row + '.0', INSERT)))
        menu_x = self.root.winfo_x() +\
            FONT_SIZE * (len(self.get(row + '.0', INSERT)) + 1)

        menu_y = self.root.winfo_y() + FONT_SIZE * int(row)

        self.sugg_menu.tk_popup(x=menu_x, y=menu_y)

    def get_start_pos(self):
        start_pos = self.index(INSERT)
        while(True):
            start_ind2 = start_pos.split('.')[1]
            start_ind2 = str(int(start_ind2) - 1)
            start_pos = start_pos.split('.')[0] + '.' + start_ind2
            if re.match(r"\s", self.get(start_pos)):
                start_ind2 = str(int(start_ind2) + 1)
                start_pos = start_pos.split('.')[0] + '.' + start_ind2
                break
            if start_ind2 == '0':
                break
        return start_pos

    def insert_w(self, w):
        print('Inserting....', w)
        self.delete(self.get_start_pos(), INSERT)
        self.insert(INSERT, w)
        print(w)
        self.sugg_menu.destroy()


    def suitable_words(self, requested_word):
        pattern = re.compile('.*' + requested_word + '.*')
        return [word for word in self.lista if re.match(pattern, word) and
                word != requested_word]

    def take_lista(self):
        try:
            written_code = ast.parse(self.get('1.0', END).strip())
            unique_lista = set()
            for node in ast.walk(written_code):
                if isinstance(node, ast.FunctionDef):
                    unique_lista.add(node.name)
                if isinstance(node, ast.Name):
                    unique_lista.add(node.id)
        except:
            print("Run time error")
        finally:
            try:
                self.lista = list(unique_lista)
            except UnboundLocalError:
                self.lista = []
