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


    # class for menu layout
    class MapMenu(tk.Frame):

        def __init__(self):
            super().__init__()

            self.MapUI()

        def MapUI(self):
            self.pack(fill=BOTH, expand=True)

            self.columnconfigure(1, weight=1)
            self.columnconfigure(3, pad=7)
            self.rowconfigure(3, weight=1)
            self.rowconfigure(5, pad=7)
            self.configure(bg='firebrick3')

            area = Text(self)
            area.grid(row=1, column=0, columnspan=2, rowspan=4,
                      padx=5, sticky=E + W + S + N)

            ## create_button = ttk.Button(self, text='Create World', command=World.random_wiggle())
            ## create_button.grid(row=1, column=3)

            ## step_button = ttk.Button(self, text='Step World', command=World.step(self))
            ## step_button.grid(row=2, column=3)

            saveMap_button = ttk.Button(self, text='Save Map', command=gif_world(w1))
            saveMap_button.grid(row=3, column=3)

            exit_button = ttk.Button(self, text='Exit', command=lambda: self.quit())
            exit_button.grid(row=5, column=3)


    def main():

        root = Tk()
        root.title('Fantorbis')
        app = MapMenu()
        root.iconbitmap(os.path.join(sys.path[0], 'images/Fantorbis-Logo.ico'))
        root.mainloop()


    if __name__ == '__main__':
        main()
