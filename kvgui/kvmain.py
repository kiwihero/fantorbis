import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from backendworld.World import World
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as kiImage
from PIL import Image, ImageDraw, ImageFont
from kivy.graphics import Color, Line, Rectangle
from io import BytesIO
# import io
from MatplotDisplay import draw_world
import copy

class UserControls(GridLayout):
    def __init__(self, active_world, display_canvas, **kwargs):
        super(UserControls, self).__init__(**kwargs)
        self.active_world = active_world
        self.display_canvas = display_canvas
        self.cols = 1
        self.rows = 5
        self.refresh_button = Button(text="Refresh display")
        self.refresh_button.bind(on_press=self.refresh_display)
        self.add_widget(self.refresh_button)
        self.subdivide_button = Button(text='Subdivide')
        self.subdivide_button.bind(on_press=self.subdivision)
        self.add_widget(self.subdivide_button)
        self.step_button = Button(text='Step')
        self.step_button.bind(on_press=self.single_step)
        self.add_widget(self.step_button)
        self.move_cell_button = Button(text='Move cell')
        self.move_cell_button.bind(on_press=self.move_cell)
        self.add_widget(self.move_cell_button)
        self.control_buttons = {
            self.subdivide_button: True,
            self.step_button: True,
            self.move_cell_button: True
        }
        self.control_button_saved_states = dict()

    def refresh_display(self, instance):
        self.disable_buttons()
        self.display_canvas.update_display(force_update=True)
        self.enable_buttons()

    def single_step(self, instance):
        self.disable_buttons()
        self.active_world.step()
        self.display_canvas.update_display()
        self.enable_buttons()
        # self.bind(size=self.update_bg)

    def subdivision(self, instance):
        self.disable_buttons()
        self.active_world.access_data_struct().subdivide()
        self.display_canvas.update_display(force_update=True)
        self.enable_buttons()

    def move_cell(self, instance):
        self.disable_buttons()
        self.active_world.access_data_struct().move_random_cell()
        self.display_canvas.update_display(force_update=True)
        self.enable_buttons()

    def disable_buttons(self):
        for button,state in self.control_buttons.items():
            self.control_button_saved_states[button] = button.disabled
            button.disabled = True

    def enable_buttons(self, force_enable: bool=False):
        for button,state in self.control_buttons.items():
            print("{} saved state {}".format(button, self.control_button_saved_states[button]))
            if force_enable is True:
                button.disabled = False
            else:
                button.disabled = self.control_button_saved_states[button]

    # def callback(self,instance):
    #     print('The button <%s> is being pressed' % instance.text)

class UserDisplayControls(GridLayout):
    def __init__(self, active_world, display_canvas, **kwargs):
        super(UserDisplayControls, self).__init__(**kwargs)
        self.active_world = active_world
        self.display_canvas = display_canvas
        self.cols = 3
        self.rows = 1

        btn1 = ToggleButton(text='speed', group='disp_controls', state='down')
        btn2 = ToggleButton(text='age_diff', group='disp_controls')
        btn3 = ToggleButton(text='stack_size', group='disp_controls')
        btn1.bind(on_press=self.request_update)
        btn2.bind(on_press=self.request_update)
        btn3.bind(on_press=self.request_update)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)

    def request_update(self, instance):
        self.display_canvas.update_display(column=instance.text)


class WorldDisplay(Widget):
    def __init__(self, active_world, **kwargs):
        super(WorldDisplay, self).__init__(**kwargs)
        self.active_world = active_world
        self.display_type = self.active_world.conf.default_display_column
        self.update_display(column=self.display_type)


        # self.current_world_pil = self.world_to_pil()
        # self.beeld = kiImage()  # only use this line in first code instance
        # self.pil_to_canvas()
        # self.beeld.texture = im.texture
        # with self.canvas:
        #     self.canvas_image = Rectangle(texture = self.beeld.texture, pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_display(self, column=None, force_update: bool = False):
        if column is None:
            column = self.display_type
        self.current_world_pil = self.world_to_pil(column=column, force_update=force_update)
        self.display_type = column
        self.pil_to_canvas()
        with self.canvas:
            self.canvas_image = Rectangle(texture=self.beeld.texture, pos=self.pos, size=self.size)

    def update_bg(self, *args):


        self.canvas_image.pos = self.pos
        self.canvas_image.size = self.size
        self.canvas_image.texture = self.beeld.texture

    def world_to_pil(self, column=None, force_update: bool = False):
        # print("root of widget {}".format(self.get_root_window()))
        # print("active world {}".format(self.active_world))
        drawn = draw_world(self.active_world,column=column, force_draw=force_update)
        canvas_img = drawn
        # canvas_img.show()
        return canvas_img

    def pil_to_canvas(self, pil=None):
        if pil is not None:
            self.current_world_pil = pil
        # print("PIL image type {} is {}".format(type(self.current_world_pil),self.current_world_pil))

        # with io.BytesIO() as output:
        #     self.current_world_pil.save(output, format="png")
        #     data = output.getvalue()
        data = BytesIO()
        self.current_world_pil.save(data, format='png')
        data.seek(0)
        # print("data type {} is {}".format(type(data), data))
        im = CoreImage(BytesIO(data.read()),ext='png')
        # print("Core image type {} is {}".format(type(im),im))
        self.beeld = kiImage()  # only use this line in first code instance
        self.beeld.texture = im.texture
        return im

class MainScreen(GridLayout):
    def __init__(self, active_world, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.active_world = active_world

        self.cols = 2

        self.world_canvas = WorldDisplay(self.active_world)
        self.add_widget(self.world_canvas)
        self.basic_controls = UserControls(self.active_world,self.world_canvas)
        self.add_widget(self.basic_controls)
        self.basic_display_controls = UserDisplayControls(self.active_world,self.world_canvas)
        self.add_widget(self.basic_display_controls)
        self.quit_button = Button(text="quit")
        self.quit_button.bind(on_release=self.quit_app)
        self.add_widget(self.quit_button)

    def quit_app(self, instance):
        App.get_running_app().stop()

class MapApp(App):
    def __init__(self, **kwargs):
        super(MapApp, self).__init__(**kwargs)
        self.active_world = World()
        self.active_conf = self.active_world.conf

    def build(self):
        self.root = root = RootWidget(self.active_world)
        return root

class RootWidget(FloatLayout):

    def __init__(self, active_world, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        self.active_world = active_world

        # let's add a Widget to this layout
        self.main_screen = MainScreen(self.active_world)
        self.add_widget(self.main_screen)









if __name__ == '__main__':
    MapApp().run()