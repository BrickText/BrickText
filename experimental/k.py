from tkinter import *

root = Tk()
t = Text(root)
t.insert(END, '''\
blah blah blah Failed blah blah
blah blah blah Passed blah blah
blah blah blah Failed blah blah
blah blah blah Failed blah blah
''')
t.tag_config('failed', background='red')
t.tag_config('passed', background='blue')


def search(text_widget=t, keyword='F', tag='failed'):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)
    t.after(0, search)


t.after(0, search)

# while True:
    # print(t.get('1.0', END))
t.pack()
root.mainloop()