import tkinter as tk
import os
import sys
from os.path import abspath,dirname
from inspect import stack
from tkinter.ttk import *
from tkinter import filedialog, ttk

# security to prevent python from writing cache files
sys.dont_write_bytecode = True

# application path
path_app = dirname(abspath(stack()[0][1]))

if path_app not in sys.path:
    sys.append(path_app)


class MainWindow(tk.Tk): #function and controls needed for main window
    def __init__(self,path_app):
        super().__init__()
        self.title('Fantorbis')
        self.iconbitmap(os.path.join(sys.path[0], 'Fantorbis-Logo.ico'))


class MapMenu(Frame): #menu for map
    def __init__(self, mapwindow):
        super.__init__(mapwindow)
        self.configure(bg="firebrick3")  # background color

        map_management = ttk.Labelframe(
            self,
            text = 'Map management',
            padding = (4,4,8,8)
        )
        map_management.grid(row=2, column=0, padx=5, pady=5)

        delete_map = ttk.Button(
            self,
            text='Delete map',
            command=mapwindow.map.delete_map,
            width=20
        )
        delete_map.grid(row=0, column=0, pady=5, in_= map_management)



    class Map(tk.Canvas):
        def __init__(self, mapwindow):
            super.__init__(mapwindow, bg='white', width=1300, height=800)
            self.ratio, self.offset = 1, (0, 0)
            self.mapwindow = mapwindow



if str.__eq__(__name__ ,'__main__'):
    mapwindow = MainWindow(path_app)
    mapwindow.mainloop()
