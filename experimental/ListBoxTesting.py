from tkinter import *


class ListBoxText(Text):
    def __init__(self, root, *args, **kwargs):
        Text.__init__(self, root, *args, **kwargs)
        self.root = root
        self.bind("<Control-space>", self.popup_m)

    def gen_list(self, event):
        self.lb = Listbox(self.root)
        print(self.winfo_x(), self.winfo_y())
        self.lb.place(x=10, y=23)
        self.lb.insert(END, "1")
        self.lb.insert(END, "2")
        self.lb.insert(END, "3")
        self.lb.insert(END, "4")

        self.lb.pack()

    def popup_m(self, event):
        popup = Menu(self.root, tearoff=0)
        popup.add_command(label='1')
        popup.add_command(label='2')
        popup.add_command(label='3')
        # popup.pack()
        print(event.x_root, event.x_root)
        print(self.root.winfo_x(), self.root.winfo_y())
        print(self.index(INSERT))
        print('-----------------------')
        add_to_x = int(self.index(INSERT).split('.')[1]) * 10
        add_to_y = (int(self.index(INSERT).split('.')[0]) + 1) * 5
        popup.tk_popup(self.root.winfo_x() + add_to_x, self.root.winfo_y() + add_to_y, 0)


def main():
    root = Tk()
    txt = ListBoxText(root)
    txt.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
