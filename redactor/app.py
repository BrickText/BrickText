from tkinter import *
from redactor.TextEditor import TextEditor


def refresher(root):
    """
    The main block which will operate with the text in the editor
    """
    root.after(0, refresher(root))


def main():
    editor = TextEditor()
    editor.start()


if __name__ == '__main__':
    main()
