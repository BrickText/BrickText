#!/usr/bin/python3
from tkinter import *
from sys import argv
import os
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.system('export PYTHONPATH=/usr/bin/python3:' +
          os.path.dirname(os.path.realpath(__file__)))

from redactor.TextEditor import TextEditor
from redactor.menu.AppMenu import AppMenu
from redactor.ResizingCanvas import ResizingCanvas
from redactor.coloring.Coloring import Coloring
from redactor.set_lines.Lines import Lines
from redactor.tree.Tree import Tree
from redactor.settings.SettingsVariables import settings
from redactor.settings.LanguageSettings import languages


def refresher(root, colors, lines, menu):
    """
    The main block which will operate with the text in the editor
    """
    if menu.color_keyword and menu.keyword:
        with open('settings/{}_keywords.json'
                  .format(languages[menu.get_file_language()])) as data_file:
            keywords = eval(data_file.read())
        keywords[menu.keyword] = menu.color_keyword
        with open('settings/{}_keywords.json'
                  .format(languages[menu.get_file_language()]),
                  'w') as data_file:
            data_file.write(json.dumps(keywords))
        colors.reset_tags(languages[menu.get_file_language()])
        menu.color = None
        menu.keyword = None
    lines.updateAllLineNumbers()
    colors.findall()
    root.after(200, refresher, root, colors, lines, menu)


def main():
    editor = TextEditor()
    ResizingCanvas(editor.get_text_panel(), editor.get_root(),
                   width=settings["DEFAULT_WIDTH"],
                   height=settings["DEFAULT_WIDTH"],
                   bg="red")
    colors = Coloring(editor, 'blank')
    tree = Tree(editor, editor.get_root(), './', colors)
    lines = Lines(editor.get_root(), editor.get_text_panel())
    menu = AppMenu(editor.get_root(), editor.get_text_panel(), colors,
                   editor, lines)
    if len(argv) > 1:
        print(argv[1])
        cwd = os.getcwd()
        path = cwd + '/' + argv[1]
        contents = ''
        with open(path, "r+") as f:
            contents = f.read()
        editor.get_text_panel().insert('1.0', contents)
        editor.set_filename(path)
        colors.reset_tags(languages[menu.get_file_language()])
    refresher(editor.get_root(), colors, lines, menu)
    editor.start()


if __name__ == '__main__':
    main()