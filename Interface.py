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
from PillowDisplay import draw_world, gif_world, image_world, _save_image

import os
import sys
import PIL.Image
import PIL.ImageTk
from PIL import ImageGrab
from tkinter import ttk, Tk, messagebox
from tkinter import *
from tkinter import filedialog
# check if user has a older version of python
if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk


    # class for main window Frame
    class MainWindow(tk.Frame):
        def __init__(self):
            super().__init__()

            self.MapUI()

            # area for map display
            self.map_canvas = Canvas(self)
            self.map_canvas.grid(row=1, column=0, columnspan=2, rowspan=4,
                       padx=5, sticky=tk.E + tk.W + tk.S + tk.N)
            self.world = None
            self.backgroundphoto = None

            # master is referring to the base widget - may change to dropdown menu
            settings_menu = Menu(self.master)
            self.master.config(menu=settings_menu)

            # create the file object)
            settings = Menu(settings_menu)
            settings_menu.add_cascade(label="Settings", menu=settings)
           # settings.add_command(label="Subdivide", command=self.subdivide_world())



        def MapUI(self):
            self.pack(fill=tk.BOTH, expand=True)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(3, pad=7)
            self.rowconfigure(3, weight=1)
            self.rowconfigure(5, pad=7)
            self.configure(bg='firebrick3')


            draw_icon = PhotoImage(file='images/pencil.png')
            self.draw_icon = draw_icon
            create_button = tk.Button(self, image=draw_icon, width=50, height=50, command=lambda: self.create_world())
            create_button.grid(row=2, column=3)

            step_button = tk.Button(self, text='Step World', command=lambda: self.stepping_world())
            step_button.grid(row=3, column=3)

            subdivide_button = tk.Button(self, text='Subdivide', command=lambda: self.subdivide_world())
            subdivide_button.grid(row=3, column=4)

            move_button = tk.Button(self, text='Move', command=lambda: self.move_world())
            move_button.grid(row=3, column=5)


            save_icon = PhotoImage(file='images/download.png')
            self.save_icon = save_icon
            saveMap_button = tk.Button(self, image=save_icon,  width=50, height=50, command=lambda: self.save_world())
            saveMap_button.grid(row=4, column=3)

            help_icon = PhotoImage(file='images/help.png')
            self.help_icon = help_icon
            help_button = Button(self, image=help_icon,  width=50, height=50,  command=lambda: self.help())
            help_button.grid(row=5, column=0, padx=5)

            exit_icon = PhotoImage(file='images/exit.png')
            self.exit_icon = exit_icon
            exit_button = tk.Button(self, image=exit_icon, width=50, height=50, command=lambda: self.quit())
            exit_button.grid(row=5, column=3)

        def create_world(self):
            print("creating world")
            interface_new_world = World()
            self.world = interface_new_world
            image_world(self.world)

            last_key = max(self.world.images.keys())
            first_image_bg = self.world.images[last_key]
            first_image_bg = PIL.Image.Image.resize(first_image_bg, (900, 600))
            photo_image = PIL.ImageTk.PhotoImage(first_image_bg)


            background_label = Label(self.map_canvas, image=photo_image)
            background_label.photo = photo_image
            background_label.grid()
            print("Canvas has {}".format(self.map_canvas))
            print("Background has {}".format(background_label.photo))
            self.backgroundphoto = background_label




        def stepping_world(self):
            print("CALLED STEPPING WORLD")
            image_world(self.world)
            #self.world.access_data_struct().subdivide()
            #self.world.random_wiggle()
            step_world = self.world.step()
            draw_world(self.world)
            print("world age {}".format(self.world.age))
            # World.step(step_world)
            # World.random_wiggle()
            last_key =max(self.world.images.keys())
            print("last key {}".format(last_key))
            first_image_bg = self.world.images[max(self.world.images.keys())]
            # self.world.images[max(self.world.images.keys())].show()
            first_image_bg = PIL.Image.Image.resize(first_image_bg, (900, 600))
            photo_image = PIL.ImageTk.PhotoImage(first_image_bg)
            # photo_image.show()
            # photo_image.grid(row=1,column=1)


            # background_label = Label(self.map_canvas, image=photo_image)
            # background_label.photo = photo_image
            # background_label.grid()
            self.backgroundphoto.configure(image=photo_image)
            self.backgroundphoto.image = photo_image

        def subdivide_world(self):
            #subdivide 3 times
         for i in range(3):
             image_world(self.world)
            #messagebox.showwarning("Subdivide warning", "Can only subdivide less than 5 times.")
             self.world.access_data_struct().subdivide()

        def move_world(self):
            print("MOVE WORLD")
            image_world(self.world)
            self.world.random_wiggle()
            World.random_wiggle()

        def save_world(self):
            first_image_bg = self.world.images[max(self.world.images.keys())]
            photo_image = PIL.ImageTk.PhotoImage(first_image_bg)
           # _save_image(photo_image,)

        def help(self):
           os.system('notepad resources/About.txt')


    class Help(tk.Frame):
        def __init__(self):
            Frame.__init__(self)

            # text area
            text_area = tk.Text(self, height=12)
            text_area.grid(column=0, row=0, sticky='nsew')

            tf = open('resources/About.txt', 'r')
            data = tf.read()
            text_area.insert(END, data)
            tf.close()


def main():
    root = Tk()
    root.title('Fantorbis')
    app = MainWindow()
    root.iconbitmap(os.path.join(sys.path[0], 'images/Fantorbis-Logo.ico'))
    root.mainloop()


if __name__ == '__main__':
             main()
