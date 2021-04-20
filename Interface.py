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
from PillowDisplay import draw_world, gif_world, image_world
from tkinterGui import Login_Window

import os
import sys
import PIL.Image
import PIL.ImageTk
from tkinter import ttk, Tk
from tkinter import *
# check if user has a older version of python
if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk

    w1 = World()

    # class for main window Frame
    class MainWindow(tk.Frame):
        def __init__(self):
            super().__init__()

            # creating entry for input
            self.num_var = tk.Entry(self)

            self.MapUI()

            # area for map display
            self.map_canvas = Canvas(self)
            self.map_canvas.grid(row=1, column=0, columnspan=2, rowspan=4,
                       padx=5, sticky=tk.E + tk.W + tk.S + tk.N)

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
            # create_button = tk.Button(self, image=draw_icon, width=50, height=50, command=World())
            create_button.grid(row=2, column=3)

            # creating a label for step value
            step_label = tk.Label(self, text=' ', font=('calibre', 10, 'bold'))
            step_label.grid(row=3, column=2)

            # creating a entry for step value
            step_entry = tk.Entry(self, textvariable=self.num_var, font=('calibre', 10, 'normal'))
            step_entry.grid(row=3, column=3)

            step_button = tk.Button(self, text='Step World', command=lambda: self.stepping_world())
            step_button.grid(row=3, column=4)


            save_icon = PhotoImage(file='images/download.png')
            self.save_icon = save_icon
            saveMap_button = tk.Button(self, image=save_icon,  width=50, height=50, command=lambda: image_world(w1))
            saveMap_button.grid(row=4, column=3)

            exit_icon = PhotoImage(file='images/exit.png')
            self.exit_icon = exit_icon
            exit_button = tk.Button(self, image=exit_icon, width=50, height=50, command=lambda: self.quit())
            exit_button.grid(row=5, column=3)

        def create_world(self):
            interface_new_world = World()
            image_world(interface_new_world)

            first_image_bg = interface_new_world.images[0]
            first_image_bg = PIL.Image.Image.resize(first_image_bg, (900, 600))
            photo_image = PIL.ImageTk.PhotoImage(first_image_bg)

            background_label = Label(self.map_canvas, image=photo_image)
            background_label.photo = photo_image
            background_label.grid()

        def stepping_world(self):
            num = self.num_var.get()
             ## print(self.num_var.get())
            step_world = World.step(num)
            World.step(step_world)




    # class for login window Frame
    # above: from tkinterGui import Login_Window

    # Still have to fix Login class so login window appears (and before interface)
    class Login:
        def __init__(self):
            super().__init__(self)

            self.login_win = Login_Window
            self.login_win.mainloop()


    def main():
        root = Tk()
        root.title('Fantorbis')
        app = MainWindow()
        root.iconbitmap(os.path.join(sys.path[0], 'images/Fantorbis-Logo.ico'))
        root.mainloop()


    if __name__ == '__main__':
        main()
