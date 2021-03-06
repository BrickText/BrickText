# TODO Ask niki for how to see if his menu is opened 

from tkinter import *
import re
import ast
import os

from redactor.settings.SettingsVariables import settings
from redactor.settings.LanguageSettings import languages

FONT_SIZE = settings["letter_size"]

class AutocompleteText(Text):
    """
        Text class which adds to your text widget AutoComplete ListBox
    """

    def __init__(self, root, *args, **kwargs):
        Text.__init__(self, root, *args, **kwargs)
        self.lista = set()
        self.root = root
        self.obj_called = False
        self.bind("<Control-space>", self.called_autocomplete)
        self.bind(".", self.called_autocomplete)
        self.bind("'", lambda _: self.add_char("'"))
        self.bind('"', lambda _: self.add_char('"'))
        self.bind("(", lambda _: self.add_char(")"))
        self.bind("[", lambda _: self.add_char("]"))
        self.bind("{", lambda _: self.add_char("}"))

    def add_char(self, w):
        pos_when_called = self.index(INSERT)
        self.insert(INSERT, w)
        self.mark_set("insert", pos_when_called)

    def called_autocomplete(self, event):
        print("autocomplete called..")
        if event.char == ".":
            self.obj_called = True

        requested_word = self.get(self.get_start_pos(), INSERT).strip()
        self.take_lista(requested_word)
        self.suggestion_menu(self.suitable_words(requested_word))

    def suggestion_menu(self, words):
        if len(words) > 0:
            self.sugg_menu = Menu(self.root, tearoff=0)
            for w in words:
                self.sugg_menu.add_command(label=w, command=lambda w=w: self.insert_w(w))
            self.position_menu()
        self.obj_called = False

    def position_menu(self):
        x, y, _, _ = self.bbox(INSERT)
        menu_x = self.root.winfo_x() + settings["side_bar_in_pixels"] + settings["letter_size"] * 4 + x
        menu_y = self.root.winfo_y() + y
        print(menu_x)
        print()
        
        self.sugg_menu.tk_popup(x=menu_x, y=menu_y)

    def get_start_pos(self):
        start_pos = self.index(INSERT)
        while True:
            start_ind2 = start_pos.split('.')[1]
            start_ind2 = str(int(start_ind2) - 1)
            start_pos = start_pos.split('.')[0] + '.' + start_ind2
            if re.match(r"\s", self.get(start_pos)) or self.get(start_pos) == '.':
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
        self.sugg_menu.destroy()
        self.obj_called = False

    def suitable_words(self, requested_word):
        if(self.obj_called):
            return [word for word in self.lista]
        else:
            pattern = re.compile('.*' + requested_word + '.*')
            return [word for word in self.lista if re.match(pattern, word) and
                    word != requested_word]

    def take_var_type(self, requested_word, parsed_code):
        for node in ast.walk(parsed_code):
            if(isinstance(node, ast.Assign)):
                if(isinstance(node.value, ast.Call)):
                    if(node.targets[0].id == requested_word):
                        return node.value.func.id

    def take_lista(self, requested_word):
        try:
            written_code = ast.parse(self.get('1.0', END).strip())
            unique_lista = set()
        
            if self.obj_called:
                class_type = self.take_var_type(requested_word, written_code)
                class_definitions = [node for node in written_code.body
                     if isinstance(node, ast.ClassDef)]
                for class_def in class_definitions:
                    if(class_type == class_def.name):
                        for node in class_def.body:
                            if isinstance(node, ast.FunctionDef):
                                unique_lista.add(node.name)
            else:
                for item in self.take_well_known_func():
                    unique_lista.add(item)
                for node in ast.walk(written_code):
                    if isinstance(node, ast.FunctionDef):
                        unique_lista.add(node.name)
                    if isinstance(node, ast.Name):
                        unique_lista.add(node.id)
                    if isinstance(node, ast.ClassDef):
                        unique_lista.add(node.name)

        except:
            print("Run time error")
        finally:
            try:
                self.lista = list(unique_lista)
            except UnboundLocalError:
                self.lista = []

    def take_well_known_func(self):
        result = []
        language = languages[settings["active_file_lang"]]
        with open(os.path.dirname(__file__) + '/../settings/{}_keywords.json'
                                             .format(language)) as data_file:
            keywords = eval(data_file.read())
        print("This")
        result = list(keywords.keys())
        print("that")
        return result
