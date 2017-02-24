from tkinter import *
from sys import argv
import os


from redactor.TextEditor import TextEditor
from menu.AppMenu import AppMenu
from redactor.ResizingCanvas import ResizingCanvas
from coloring.Coloring import Coloring
from set_lines.Lines import Lines
from settings.SettingsVariables import settings


def refresher(root, colors, lines):
    """
    The main block which will operate with the text in the editor
    """
    lines.updateAllLineNumbers()
    colors.findall()
    root.after(200, refresher, root, colors, lines)


def main():
    editor = TextEditor()
    ResizingCanvas(editor.get_text_panel(), editor.get_root(),
                   width=settings["DEFAULT_WIDTH"],
                   height=settings["DEFAULT_WIDTH"],
                   bg="red")
    lines = Lines(editor.get_root(), editor.get_text_panel())
    colors = Coloring(editor, 'python')
    menu = AppMenu(editor.get_root(), editor.get_text_panel(), colors, editor, lines)
    if len(argv) > 1:
        print(argv[1])
        cwd = os.getcwd()
        path = cwd + '/' + argv[1]
        contents = ''
        with open(path, "r+") as f:
            contents = f.read()
        editor.get_text_panel().insert('1.0', contents)
        menu.filename = path
    refresher(editor.get_root(), colors, lines)
    editor.start()


if __name__ == '__main__':
    main()
