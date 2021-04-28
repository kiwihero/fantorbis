# TODO: Interaction to generate a new world,
#  Create World()

# TODO: Interaction to step the world,
#  use step() on the world

# TODO: Interaction to save a world image/gif,
#  use something like the gif_world(World) function in PillowDisplay?

from backendworld.World import *
from PillowDisplay import draw_world, gif_world, image_world
import os
import sys
import PIL.Image
import PIL.ImageTk
from PIL import ImageGrab
from tkinter import ttk, Tk
from tkinter import *
from tkinter import filedialog
# check if user has a older version of python
if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk


    # class for main window Frame
    class MainWindow(tk.Tk):
        def __init__(self):
            super().__init__()

            self.title('Fantorbis')
            self.iconbitmap(os.path.join(sys.path[0], 'images/Fantorbis-Logo.ico'))

            self.map = Map(self)
            self.map.pack(side='right', fill='both', expand=1)

            self.mapMenu = MapMenu(self)
            self.menu.pack(side='right', fill='both', expand=1)

            self.world = None
            self.backgroundphoto = None

    class MapMenu(tk.Frame):
        def __init__(self, parent):
            tk.Frame.__init__(self, parent)
            self.parent = parent
            self.pack(fill=tk.BOTH, expand=True)

            self.columnconfigure(1, weight=1)
            self.columnconfigure(3, pad=7)
            self.rowconfigure(3, weight=1)
            self.rowconfigure(5, pad=7)
            self.configure(bg='firebrick3')

            draw_icon = PhotoImage(file='images/pencil.png')
            self.draw_icon = draw_icon
            create_button = tk.Button(self, image=draw_icon, width=50, height=50, command=parent.map.create_world())
            create_button.grid(row=2, column=3)

            step_button = tk.Button(self, text='Step World', command=parent.map.stepping_world())
            step_button.grid(row=3, column=4)

            step_button = tk.Button(self, text='Subdivide', command=parent.map.stepping_world())
            step_button.grid(row=3, column=5)

            step_button = tk.Button(self, text='Move', command=parent.map.stepping_world())
            step_button.grid(row=3, column=6)

            save_icon = PhotoImage(file='images/download.png')
            self.save_icon = save_icon
            saveMap_button = tk.Button(self, image=save_icon, width=50, height=50, command=parent.map.save_world())
            saveMap_button.grid(row=4, column=3)

            help_icon = PhotoImage(file='images/help.png')
            self.help_icon = help_icon
            help_button = Button(self, image=help_icon, width=50, height=50, command=lambda: self.help())
            help_button.grid(row=5, column=0, padx=5)

            exit_icon = PhotoImage(file='images/exit.png')
            self.exit_icon = exit_icon
            exit_button = tk.Button(self, image=exit_icon, width=50, height=50, command=self.quit())
            exit_button.grid(row=5, column=3)


    class Map(tk.Canvas):
        def __init__(self, parent):
            super().__init__(parent, bg='white', width=1300, height=800)
            self.parent = parent

            # area for map display
            self.map_canvas = Canvas(self)
            self.map_canvas.grid(row=1, column=0, columnspan=2, rowspan=4,
                                 padx=5, sticky=tk.E + tk.W + tk.S + tk.N)

            def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

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
                num = self.num_entry.get()
                self.world.access_data_struct().subdivide()
                # print(num)
                self.world.random_wiggle()
                step_world = self.world.step()
                draw_world(self.world)
                print("world age {}".format(self.world.age))
                # World.step(step_world)
                # World.random_wiggle()
                last_key = max(self.world.images.keys())
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

            def save_world(self):
                save_world_image = World()
                gif_world(save_world_image)
                myFormats = [('Portable Network Graphics', '*.png'),
                             ('JPEG', '*.jpg'), ('GIF', '*.gif'), ]
                filename = filedialog.asksaveasfilename(filetypes=myFormats)
                if not filename:
                    return
                ##self.grabcanvas.save("flatImages/out.gif")
                # save(gif_world(save_world_image))

            def help(self):
                os.system('notepad resources/About.txt')


    def main():
        root = tk.Tk()
        root.title('Fantorbis')
        #app = MainWindow()
        MainWindow(root)
        root.iconbitmap(os.path.join(sys.path[0], 'images/Fantorbis-Logo.ico'))
        root.mainloop()


        if __name__ == '__main__':
            #MainWindow().mainloop()
            main()



