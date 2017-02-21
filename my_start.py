from tkinter import *
from config_tags import config_tags
import json
from search_keywords import search

root = Tk()
t = Text(root)

config_tags(t, 'python')
# t.tag_config('failed', background='red')
# t.tag_config('passed', background='blue')

# def search(text_widget, keyword, tag):
#     pos = '1.0'
#     while True:
#         idx = text_widget.search(keyword, pos, END)
#         if not idx:
#             break
#         pos = '{}+{}c'.format(idx, len(keyword))
#         text_widget.tag_add(tag, idx, pos)


def Refresher():
    with open('{0}_keywords.json'.format(language)) as data_file:
        keywords = json.load(data_file)
    for k, _ in keywords.items():
        search(t, k, k)
    # global text
    # text.configure(text=time.asctime())
    # search(t, 'Passed', 'passed')
    root.after(1, Refresher)  # every second...


t.pack()
search(t, 'Failed', 'failed')
search(t, 'Passed', 'passed')
Refresher()

#t.tag_delete('failed')
#t.tag_delete('passed')

root.mainloop()
