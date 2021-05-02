import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from backendworld.World import World
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as kiImage
from PIL import Image, ImageDraw, ImageFont
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from io import BytesIO
# import io
from kivy.event import EventDispatcher
from MatplotDisplay import draw_world
import copy
import threading

class ThreadededFunctions():
    def __init__(self,parent_widget, root):
        self.parent_widget = parent_widget
        self.root = root
        print("root {}".format(self.root))
        # self.ev = ev = ThreadEventDispatcher()
        self.dispatcher = self.root.ev
        # self.dispatcher.bind(on_thread_completion=self.complete_thread)
        # self.background_dispatcher = ThreadedProgram(self.ev)

    def complete_thread(self, arg1=None, arg2=None, request_display_update: bool = False):
        self.dispatcher.dispatch('on_thread_completion', 'test_message')
        # if request_display_update is True:
        #     self.dispatcher.dispatch('on_display_update_request', 'test_message')
        # raise Exception

    def start_thread(self, arg1=None, arg2=None):
        self.dispatcher.dispatch('on_thread_beginning', 'test_message')



    def subdivision(self, instance=None):
        self.start_thread()
        self.parent_widget.disable_buttons()
        self.parent_widget.active_world.access_data_struct().subdivide()
        self.complete_thread()


    def move_cell(self, instance=None):
        self.start_thread()
        self.parent_widget.disable_buttons()
        self.parent_widget.active_world.force_split()
        self.complete_thread()
        # self.parent_widget.display_canvas.update_display(force_update=True)
        # self.parent_widget.enable_buttons()

    def step(self, instance=None):
        self.start_thread()
        self.parent_widget.disable_buttons()
        self.parent_widget.active_world.step()
        self.complete_thread()

    def refresh_display(self, instance=None):
        self.start_thread()
        self.parent_widget.disable_buttons()
        self.parent_widget.active_world.access_data_struct().update_cells()
        # self.parent_widget.display_canvas.update_display(force_update=True)
        self.complete_thread(request_display_update=True)


class UserControls(GridLayout):
    def __init__(self, active_world, display_canvas, root, **kwargs):
        super(UserControls, self).__init__(**kwargs)
        self.active_world = active_world
        self.display_canvas = display_canvas
        self.root = root
        self.threaded_controls = ThreadededFunctions(parent_widget=self, root=self.root)
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
        self.move_cell_button = Button(text='Force split')
        self.move_cell_button.bind(on_press=self.move_cell)
        self.add_widget(self.move_cell_button)
        self.control_buttons = {
            self.refresh_button: True,
            self.subdivide_button: True,
            self.step_button: True,
            self.move_cell_button: True
        }
        self.control_button_saved_states = dict()

    def refresh_display(self, instance):
        t1 = threading.Thread(target=self.threaded_controls.refresh_display)
        t1.start()
        self.reactivation(force_update=True)

    def update_display(self, instance=None):
        raise Exception
        self.display_canvas.update_display(force_update=True)

    def single_step(self, instance):
        t1 = threading.Thread(target=self.threaded_controls.move_cell)
        t1.start()
        Clock.schedule_once(self.reactivation)


    def subdivision(self, instance):
        t1 = threading.Thread(target=self.threaded_controls.subdivision)
        t1.start()
        Clock.schedule_once(self.reactivation)

    def move_cell(self, instance):
        t1 = threading.Thread(target=self.threaded_controls.move_cell)
        t1.start()
        Clock.schedule_once(self.reactivation)

    def disable_buttons(self):
        for button,state in self.control_buttons.items():
            self.control_button_saved_states[button] = button.disabled
            button.disabled = True

    def reactivation(self, instance=None, force_update=True):
        # print("User controls reactivation")
        if self.root.running_thread is False:
            self.display_canvas.update_display(force_update=force_update)
            # raise Exception
            self.enable_buttons()
        else:
            Clock.schedule_once(self.reactivation)

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
        # raise Exception
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
            # raise Exception
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

class MainScreen(Screen):
    def __init__(self, active_world, root, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.active_world = active_world
        self.root = root
        self.layout = MainLayout(self.active_world, self.root)





class MainLayout(GridLayout):
    def __init__(self, active_world, root, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.active_world = active_world
        self.root = root
        self.cols = 2

        self.world_canvas = WorldDisplay(self.active_world)
        self.add_widget(self.world_canvas)
        self.basic_controls = UserControls(self.active_world, self.world_canvas, root=self.root)
        self.add_widget(self.basic_controls)
        self.basic_display_controls = UserDisplayControls(self.active_world, self.world_canvas)
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

class ThreadEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_thread_completion')
        self.register_event_type('on_thread_beginning')
        self.register_event_type('on_display_update_request')
        super(ThreadEventDispatcher, self).__init__(**kwargs)

    def on_thread_completion(self, *args):
        print("Event dispatcher completion.")
        pass

    def on_thread_beginning(self, *args):
        print("Event dispatcher starting")
        # raise Exception
        pass

    def on_display_update_request(self, *args):
        print("Event dispatcher starting")
        # raise Exception
        pass

class RootWidget(FloatLayout):

    def __init__(self, active_world, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        self.active_world = active_world
        self.running_thread = False
        self.ev = ev = ThreadEventDispatcher()
        ev.bind(on_thread_beginning=self.start_running_thread)
        ev.bind(on_thread_completion=self.complete_running_thread)
        ev.bind(on_display_update_request=self.request_display_update)


        # let's add a Widget to this layout
        self.sm = ScreenManager()
        self.sm.transition = NoTransition()
        self.add_widget(self.sm)
        self.main_screen = Screen()
        self.main_layout = MainLayout(self.active_world, root=self)
        self.main_screen.add_widget(self.main_layout)
        # self.main_screen = MainScreen(self.active_world, root=self, name="main")
        self.sm.add_widget(self.main_screen)
        print("sm curr {}".format(self.sm.current_screen))

    def start_running_thread(self, arg1=None, arg2=None):
        self.running_thread = True
        # raise Exception



    def complete_running_thread(self, arg1=None, arg2=None):
        self.running_thread = False
        # raise Exception

    def request_display_update(self, arg1=None, arg2=None):
        if self.running_thread is False:
            self.main_layout.basic_controls.update_display()
        else:
            print("Cannot request update, thread is still running")
            raise Exception
            Clock.schedule_once(self.request_display_update)











if __name__ == '__main__':
    MapApp().run()