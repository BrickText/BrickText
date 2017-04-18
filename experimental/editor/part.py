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

def search(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)

def Refresher():
    # global text
    # text.configure(text=time.asctime())
    search(t, 'Passed', 'passed')
    root.after(1000, Refresher) # every second...

t.pack()
search(t, 'Failed', 'failed')
search(t, 'Passed', 'passed')
Refresher()

#t.tag_delete('failed')
#t.tag_delete('passed')

root.mainloop()
