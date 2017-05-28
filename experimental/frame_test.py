from tkinter import *


def main():
    root = Tk()
    frame = Frame(height=200, width=300, bd=1, relief=SUNKEN)
    frame.pack()
    print(frame.winfo_width(), frame.winfo_height())
    mainloop()


if __name__ == '__main__':
    main()
