from tkinter import *

from redactor.TextEditor import TextEditor
from menu.AppMenu import AppMenu
from redactor.ResizingCanvas import ResizingCanvas
from coloring.Coloring import Coloring

# Move to setting file

DEFAULT_WIDTH = 850
DEFAULT_HEIGHT = 400


def refresher(root):
    """
    The main block which will operate with the text in the editor
    """
    root.after(0, refresher(root))


def main():
    editor = TextEditor()
    ResizingCanvas(editor.get_text_panel(),
                   width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                   bg="red")
    AppMenu(editor.get_root(), editor.get_text_panel())
    Coloring(editor, 'python')
    editor.start()


if __name__ == '__main__':
    main()
