from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as tkFileDialog
import os
# import Image, ImageTk


VERSION = "v0.0.3"


"""
folderDialog Class

Dialog that asks the user to select a folder. Returns folder and gets destroyed.

"""
class folderDialog(Toplevel):
    def __init__(self, parent, callback, dir="./", fileFilter=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        self.title("Browse Folders")
        self.parent = parent
        self.dir = StringVar()
        self.callback = callback
        self.fileFilter = fileFilter

        if os.path.exists(dir) and os.path.isdir(dir):
            self.dir.set(os.path.abspath(dir))
        else:
            self.dir.set(os.path.abspath("./"))

        self.body = Frame(self)
        self.body.grid(row=0,column=0,padx=5,pady=5, sticky=(N,S,E,W))

        Label(self.body, text="Please select a folder").grid(row=0,column=0, sticky=(N,S,W), pady=3)
        Label(self.body, text="You are in folder:").grid(row=1,column=0, sticky=(N,S,W))
        Entry(self.body, textvariable=self.dir, state="readonly").grid(row=2,column=0,sticky=(N,S,E,W),columnspan=2)
        self.treeview = Treeview(self.body, columns=("dir", "imgs"), show="headings")
        self.treeview.grid(row=3,column=0,sticky=(N,S,E,W),rowspan=3,pady=5,padx=(0,5))

        self.treeview.column("imgs", width=30, anchor=E)
        self.treeview.heading("dir", text="Select a Folder:", anchor=W)
        self.treeview.heading("imgs", text="Image Count", anchor=E)
        #self.treeview.heading(0, text="Select Directory")
        #self.listbox = Listbox(self.body, activestyle="dotbox", font=("Menu", 10))
        #self.listbox.grid(row=3,column=0, sticky=(N,S,E,W),rowspan=3,pady=5,padx=(0,5))

        ok = Button(self.body, text="Use Folder")
        ok.grid(row=3,column=1,sticky=(N,E,W), pady=5)

        cancel = Button(self.body, text="Cancel")
        cancel.grid(row=4,column=1,sticky=(N,E,W), pady=5)        

        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Escape>", self.cancel)
        cancel.bind("<Button-1>", self.cancel)
        ok.bind("<Button-1>", self.selectFolder)
        self.treeview.bind("<Left>", self.newFolder)
        self.treeview.bind("<Right>", self.newFolder)
        self.treeview.bind("<Return>", self.selectFolder)
        self.treeview.bind("<Up>", self.onUpDown)
        self.treeview.bind("<Down>", self.onUpDown)
        self.treeview.bind("<<TreeviewSelect>>", self.onChange)

        self.geometry("%dx%d+%d+%d" % (450, 400,
            parent.winfo_rootx()+int(parent.winfo_width()/2 - 200),
            parent.winfo_rooty()+int(parent.winfo_height()/2 - 150)
        ))

        self.updateListing()
        self.treeview.focus_set()
        self.resizable(0,0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(5, weight=1)

        self.wait_window(self)

    def newFolder(self, event):
        newDir = self.dir.get()
        if event.keysym == "Left":
            #newDir = os.path.join(newDir, "..")
            self.upFolder()
            return
        else:
            selected = self.getSelected()

            if selected == ".":
                #special super cool stuff here
                self.selectFolder()
                return
            elif selected == "..":
                self.upFolder()
                return
            else:
                newDir = os.path.join(newDir, selected)

        self.dir.set(os.path.abspath(newDir))
        self.updateListing()

    def upFolder(self):
        cur = os.path.split(self.dir.get())
        newDir = cur[0]
        cur = cur[1]

        self.dir.set(os.path.abspath(newDir))
        self.updateListing()

        children = self.treeview.get_children()
        for child in children:
            if self.treeview.item(child, "text") == cur:
                self.treeview.selection_set(child)
                self.treeview.focus(child)
                #print "please see"
                self.treeview.see(child)
                return

    def onChange(self, event=None):
        #print event
        sel = self.treeview.focus()
        if sel == '':
            return #not possible, but just in case

        if self.treeview.item(sel, "values")[1] == "?":
            #print "Has ?"
            self.imgCount()

    def imgCount(self):      
        folder = os.path.join(self.dir.get(), self.getSelected())
        folder = os.path.abspath(folder)

        count = 0

        dirList = os.listdir(folder)
        for fname in dirList:
            if self.fileFilter == None:
                count = count + 1
            else:
                ext = os.path.splitext(fname)[1].lower()[1:]
                #print ext
                for fil in self.fileFilter:
                    #print fil
                    if ext == fil:
                        count = count + 1
                        break

        #print count
        sel = self.treeview.focus()  
        newV = (self.treeview.item(sel, "values")[0], str(count))
        self.treeview.item(sel, value=newV)


    def onUpDown(self, event):
        sel = self.treeview.selection()
        if len(sel) == 0:
            return
        active = self.treeview.index(sel[0])
        children = self.treeview.get_children()
        length = len(children)
        toSelect = 0
        if event.keysym == "Up" and active == 0:
            toSelect = length - 1
        elif event.keysym == "Down" and active == length-1:
            toSelect = 0
        else:
            return

        toSelect = children[toSelect]
        self.treeview.selection_set(toSelect)
        self.treeview.focus(toSelect)
        self.treeview.see(toSelect)
        return 'break'


    def updateListing(self, event=None):
        folder = self.dir.get()
        children = self.treeview.get_children()
        for child in children:
            self.treeview.delete(child)
        #self.treeview.set_children("", '')
        dirList = os.listdir(folder)

        first = self.treeview.insert("", END, text=".", values=("(.) - Current Folder", "?"))
        self.treeview.selection_set(first)
        self.treeview.focus(first)

        self.treeview.insert("", END, text="..", values=("(..)", "?"))
        #self.listbox.insert(END, "(.) - Current Folder")
        #self.listbox.insert(END, "(..)")
        for fname in dirList:
            if os.path.isdir(os.path.join(folder, fname)):
                #self.listbox.insert(END,fname+"/")
                self.treeview.insert("", END, values=(fname+"/", "?"), text=fname)

    def selectFolder(self, event=None):
        selected = os.path.join(self.dir.get(), self.getSelected())
        selected = os.path.abspath(selected)
        self.callback(selected, self)
        self.cancel()

    def getSelected(self):
        selected = self.treeview.selection()

        if len(selected) == 0:
            selected = self.treeview.identify_row(0)
        else:
            selected = selected[0]

        return self.treeview.item(selected, "text")

    def ok(self):

        #print "value is", self.e.get()

        self.top.destroy()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()




"""
Img Class

Stores path to img and manipulates (resizes).

"""
class Img:
    def __init__(self, path):
        self.path = path
        self.size = 0,0
        self.oSize = 0,0
        self.img = None
        self.tkpi = None

        split = os.path.split(self.path)
        self.folderName = os.path.split(split[0])[1]
        self.fileName = split[1]

        self.stats()
        #print "Loaded " + path
        self.img = None

    def stats(self):
        self.img = Image.open(self.path)
        self.size = self.img.size
        self.oSize = self.img.size

    def load(self):
        self.img = Image.open(self.path)#.convert("RGB") #RGB for better resizing
        #print self.img.mode
        if self.img.mode == "P":
            self.img = self.img.convert("L") #L scales much more nicely than P

    def unload(self):
        self.img = None
        self.tkpi = None
        self.size = self.oSize

    def fit(self, size):
        #ratio = min(1.0 * size[0] / self.oSize[0], 1.0 * size[1] / self.oSize[1])
        ratio = 1.0 * size[0] / self.oSize[0]
        ratio = min(ratio, 1.0)
        #print ratio
        self.size = (int(self.oSize[0] * ratio), int(self.oSize[1] * ratio))
        #print self.size

    def resize(self, size):
        #self.fit(size)
        self.load()
        self.img = self.img.resize(self.size, Image.BICUBIC)
        #self.img = self.img.resize(self.size, Image.ANTIALIAS)
        self.tkpi = ImageTk.PhotoImage(self.img)
        return self.tkpi

    def quickResize(self, size):
        self.fit(size)
        if self.img == None:
            self.load()
        self.img = self.img.resize(self.size)
        self.tkpi = ImageTk.PhotoImage(self.img)
        return self.tkpi





"""
MangaViewer Class

The main class, runs everything.

"""
class MangaViewer:
    def __init__(self, root):
        self.root = root
        self.setTitle(VERSION)
        root.state("zoomed")

        self.frame = Frame(self.root)#, bg="#333333")#, cursor="none")
        self.canvas = Canvas(self.frame,xscrollincrement=15,yscrollincrement=15,bg="#1f1f1f", highlightthickness=0)
        scrolly = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=scrolly.set)

        #self.img = Image.open("C:\\Users\\Alex\\Media\\manga\\Boku wa Tomodachi ga Sukunai\\16\\02-03.png")
        #self.tkpi = ImageTk.PhotoImage(self.img)
        #self.imgId = self.canvas.create_image(0,0, image=self.tkpi, anchor="nw")
        #self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
        self.files = []
        self.current = 0

        self.canvas.bind("<Configure>", self.onConfig)
        self.root.bind("<Up>", self.onScroll)
        self.root.bind("<Down>", self.onScroll)
        self.root.bind("<Left>", self.onNewImg)
        self.root.bind("<Right>", self.onNewImg)
        self.root.bind("<d>", self.getNewDirectory)
        self.root.bind("<f>", self.toggleFull)
        self.root.bind("<Motion>", self.onMouseMove)
        #Windows
        self.root.bind("<MouseWheel>", self.onMouseScroll)
        # Linux
        self.root.bind("<Button-4>", self.onMouseScroll)
        self.root.bind("<Button-5>", self.onMouseScroll)
        self.root.bind("<Escape>", lambda e: self.root.quit())

        self.frame.grid(column=0, row=0, sticky=(N,S,E,W))
        self.canvas.grid(column=0,row=0, sticky=(N,S,E,W))
        #scrolly.grid(column=1, row=0, sticky=(N,S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.resizeTimeO = None
        self.mouseTimeO = self.root.after(1000, lambda x: x.frame.configure(cursor="none"), self)
        self.lastDir = os.path.abspath("./")
        self.imgId = None
        self.fullscreen = False

    def toggleFull(self, event=None):
        if self.fullscreen:
            root.overrideredirect(False)
        else:
            root.overrideredirect(True)

        self.fullscreen = not self.fullscreen
        self.onConfig(None)

    def setTitle(self, *titles):
        st = ""
        for title in titles:
            st = st + " " + str(title)
        self.root.title("MangaViewer  - " + st)

    def setTitleToImg(self):
        self.setTitle(self.files[self.current].folderName,"-", 
            self.files[self.current].fileName,"(",(self.current+1),"/",len(self.files),")")

    def onMouseMove(self, event):
        """hide cursor after some time"""

        #print event
        self.frame.configure(cursor="")
        if self.mouseTimeO != None:
            self.root.after_cancel(self.mouseTimeO)
        self.mouseTimeO = self.root.after(1000, lambda x: x.frame.configure(cursor="none"), self)

    def onMouseScroll(self, event):
        #mousewheel for windows, mousewheel linux, or down key
        if event.num == 4 or event.delta == 120:
            self.canvas.yview("scroll", -3, "units")
        else:
            self.canvas.yview("scroll", 3, "units")

    def onScroll(self, event):
        """called when the up or down arrow key is pressed"""

        if event.keysym == "Down":
            self.canvas.yview("scroll", 1, "units")
        else:
            self.canvas.yview("scroll", -1, "units")

    def onNewImg(self, event):
        """called when the left or right arrow key is pressed, changes the image"""

        change = 1 #right key
        if event.keysym == "Left":
            change = -1

        newImg = self.current + change
        if newImg < 0 or newImg >= len(self.files):
            self.getNewDirectory()
            return

        #self.img = self.files[newImg];
        #self.tkpi = ImageTk.PhotoImage(self.img)
        #self.canvas.delete(self.imgId)
        #self.imgId = self.canvas.create_image(0,0, image=self.tkpi, anchor="nw")
        #self.canvas.configure(scrollregion=self.canvas.bbox(ALL)) #needed?
        self.files[self.current].unload()
        self.current = newImg
        self.setTitleToImg()
        self.onConfig(None, True)

    def getNewDirectory(self, event=None):
        folderDialog(self.root, self.selNewDirectory, self.lastDir, fileFilter=["jpg", "png", "gif", "jpeg"])


    def selNewDirectory(self, dirname, fd):
        """callback given to folderDialog"""

        fd.cancel() #destroy the folderDialog

        if self.lastDir == dirname:
            return

        self.lastDir = dirname
        #print dirname
        dirList = os.listdir(dirname)
        self.files = []
        self.current = -2
        for fname in dirList:
            ext = os.path.splitext(fname)[1].lower()
            if ext == ".png" or ext == ".jpg" or ext == ".jpeg" or ext == ".gif":
                self.files.append(Img(os.path.join(dirname, fname)))
        self.current = 0
        if len(self.files) == 0:
             return
        self.setTitleToImg()
        self.onConfig(None, True)

    def resize(self, finalResize=False):
        """resizes the image"""

        canvasSize = (self.canvas.winfo_width(), self.canvas.winfo_height())
        tkpi = None
        if finalResize:
            tkpi = self.files[self.current].resize(canvasSize)
        else:
            tkpi = self.files[self.current].quickResize(canvasSize)

            if self.resizeTimeO != None: #is this the best way to do this?
                self.root.after_cancel(self.resizeTimeO)
            self.root.after(200, self.onConfig, None, True)

        if self.imgId != None:
            self.canvas.delete(self.imgId)

        self.imgId = self.canvas.create_image(0,0, image=tkpi, anchor="nw")
        #self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
        bbox = self.canvas.bbox(ALL)
        #nBbox = (bbox[0], bbox[1]-60, bbox[2], bbox[3]+60)
        nBbox = bbox
        self.canvas.configure(scrollregion=nBbox)
        #print self.canvas.bbox(ALL)

    def onConfig(self, event, finalResize=False):
        """runs the resize method and centers the image"""

        if self.current < 0 or self.current >= len(self.files):
            return

        self.canvas.yview("moveto", 0.0)
        self.resize(finalResize)

        newX = (self.canvas.winfo_width() - self.files[self.current].size[0])/2
        #newY - 60 TODO change to preference padding
        newY = (self.canvas.winfo_height() - self.files[self.current].size[1])/2# - 60
        newY = max(newY, 0)

        self.canvas.coords(self.imgId, newX, newY)
        self.canvas.yview("moveto", 0.0)
        bbox = self.canvas.bbox(ALL)
        nbbox = (0,0, bbox[2], max(bbox[3], self.canvas.winfo_height()))
        self.canvas.configure(scrollregion=nbbox)

root = Tk()
Frame(root)
root.mainloop()