"""
This is where the backend and ui interface
"""
# TODO: Interaction to generate a new world,
#  Create World()

# TODO: Interaction to step the world,
#  use step() on the world

# TODO: Interaction to save a world image/gif,
#  use something like the gif_world(World) function in PillowDisplay?

from backendworld.World import *
from PillowDisplay import draw_world, gif_world,image_world
import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
# check if user has a older version of python
if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk

    w1 = World()

    root = tk.Tk()
    root.wm_title('Fantorbis')
    root.iconbitmap(os.path.join(sys.path[0], 'images/Fantorbis-Logo.ico'))




    saveMap_button = ttk.Button(root, text='Save Map', command=gif_world(w1)).grid(row=0, column=0)
    exit_button = ttk.Button(root,text='Exit',command=lambda: root.quit()).grid(row=0, column=3)

root.mainloop()