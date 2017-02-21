from tkinter import *

def main(a_list):
    def show_entry_fields():
       print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

    master = Tk()
    Label(master, text="First Name").grid(row=0)
    Label(master, text="Last Name").grid(row=1)

    e1 = Entry(master)
    e2 = Entry(master)


    a = e1.get()
    print(type(a), a)
    a_list.append(a)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
    Button(master, text='Show', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)

    mainloop()


if __name__ == '__main__':
    a_list = []
    main(a_list)
    print(a_list)
