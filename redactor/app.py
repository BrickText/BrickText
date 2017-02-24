from tkinter import *

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
    AppMenu(editor.get_root(), editor.get_text_panel(), colors, editor, lines)
    refresher(editor.get_root(), colors, lines)
    editor.start()


if __name__ == '__main__':
    main()
