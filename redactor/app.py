from tkinter import *

from redactor.TextEditor import TextEditor
from menu.AppMenu import AppMenu
from redactor.ResizingCanvas import ResizingCanvas
from coloring.Coloring import Coloring
from set_lines.Lines import Lines

# Move to setting file

DEFAULT_WIDTH = 850
DEFAULT_HEIGHT = 400


def refresher(root, colors, lines):
    """
    The main block which will operate with the text in the editor
    """
    lines.updateAllLineNumbers()
    colors.findall()
    root.after(200, refresher, root, colors, lines)


def main():
    editor = TextEditor()
    ResizingCanvas(editor.get_text_panel(),
                   width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                   bg="red")
    AppMenu(editor.get_root(), editor.get_text_panel())
    lines = Lines(editor.get_root(), editor.get_text_panel())
    colors = Coloring(editor, 'python')
    refresher(editor.get_root(), colors, lines)
    editor.start()


if __name__ == '__main__':
    main()
