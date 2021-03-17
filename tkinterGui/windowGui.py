from tkinter import *
import os

import tk


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        menu = Menu(self.master)
        self.master.config(menu=menu)

        filemenu = Menu(menu)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)
        filemenu.add_command(label="Close", command=donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menu)
        helpmenu.add_command(label="About...", command=about)
        menu.add_cascade(label="Help", menu=helpmenu)


def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin, text="Do nothing button")
    button.pack()



def about():
    os.system('notepad tkinterGui/About.txt')



root = Tk()
app = Window(root)
root.wm_title("Fantorbis")

#Setting Icon for window widget
#root.iconbitmap(r'C:\Users\ashnf\fantorbis\images\favicon.ico')
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='images/bitmap.png'))

root.mainloop()






