import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
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
from MatplotDisplay import draw_world, draw_plates
import copy
import threading

from kvgui.customkvclasses import ExtendedButton, IntInput

class ThreadededFunctions():
    def __init__(self,parent_widget, root):
        self.parent_widget = parent_widget
        self.root = root
        print("root {}".format(self.root))
        # self.ev = ev = ThreadEventDispatcher()
        self.dispatcher = self.root.ev
        self.step_textbox = 0
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

    def step_many(self, instance=None, steps_requested=1):
        print("step many; textbox {}".format(self.step_textbox))
        self.start_thread()
        self.parent_widget.disable_buttons()
        for s in range(int(self.step_textbox)):
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
        self.step_layout = BoxLayout(orientation='horizontal')
        self.step_button = Button(text="Step")
        self.add_widget(self.step_layout)
        self.step_layout.add_widget(self.step_button)
        self.step_button.bind(on_press=self.single_step)
        self.multi_step_button = Button(text="Multi-step")
        self.multi_step_button.bind(on_press=self.multi_step)
        self.multi_step_input = IntInput(multiline=False)
        self.multi_step_input.bind(on_text_validate=self.on_enter)
        self.step_layout.add_widget(self.multi_step_input)
        self.step_layout.add_widget(self.multi_step_button)
        # TODO: Multi-select button
        # self.extended_step_button = ExtendedButton(main_button=self.step_button, dropdown_buttons=[self.multi_step_button])
        # self.extended_step_button.main_button.
        # self.add_widget(self.extended_step_button)
        self.move_cell_button = Button(text='Force split')
        self.move_cell_button.bind(on_press=self.move_cell)
        self.add_widget(self.move_cell_button)
        self.control_buttons = {
            self.refresh_button: True,
            self.subdivide_button: True,
            self.step_button: True,
            self.multi_step_input: True,
            self.multi_step_button: True,
            self.move_cell_button: True
        }
        self.control_button_saved_states = dict()

    def reset_world(self, world):
        self.active_world = world

    def refresh_display(self, instance):
        t1 = threading.Thread(target=self.threaded_controls.refresh_display)
        t1.start()
        self.reactivation(force_update=True)

    def update_display(self, instance=None):
        raise Exception
        self.display_canvas.update_display(force_update=True)

    def single_step(self, instance):
        t1 = threading.Thread(target=self.threaded_controls.step)
        t1.start()
        Clock.schedule_once(self.reactivation)



    def on_enter(self, instance):
        self.threaded_controls.step_textbox = int(instance)
        self.multi_step(steps=int(instance))


    def multi_step(self, instance=None, steps=None):
        self.threaded_controls.step_textbox = int(self.multi_step_input.text)
        t1 = threading.Thread(target=self.threaded_controls.step_many)
        t1.start()
        self.multi_step_input.text = ''
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
            current_control = self.root.main_layout.basic_display_controls.disp_controls_state
            current_plate =self.root.main_layout.basic_display_controls.plate_controls_state
            self.display_canvas.update_display(force_update=force_update, column=current_control, plate_control=current_plate)
            print("current control {}, plate {}".format(current_control, current_plate))
            # raise Exception
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
        self.rows = 2

        self.btn1 = btn1 = ToggleButton(text='speed', group='disp_controls', state='down')
        self.btn2 = btn2 = ToggleButton(text='age_diff', group='disp_controls')
        self.btn3 = btn3 = ToggleButton(text='stack_size', group='disp_controls')
        self.btn4 = btn4 = ToggleButton(text='default_plates', group='plate_controls',state='down')
        self.btn5 = btn5 = ToggleButton(text='plates_only', group='plate_controls')
        self.btn5 = btn6 = ToggleButton(text='no_plates', group='plate_controls')
        btn1.bind(on_press=self.request_update)
        btn2.bind(on_press=self.request_update)
        btn3.bind(on_press=self.request_update)
        btn4.bind(on_press=self.request_update)
        btn5.bind(on_press=self.request_update)
        btn6.bind(on_press=self.request_update)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)
        self.add_widget(btn4)
        self.add_widget(btn5)
        self.add_widget(btn6)
        self.disp_controls_state = self.active_world.conf.default_controls_state
        self.plate_controls_state = self.active_world.conf.default_plates_state

    def reset_world(self, world):
        self.active_world = world

    def request_update(self, instance):
        if instance.group == 'disp_controls':
            self.disp_controls_state = instance.text
        if instance.group == 'plate_controls':
            self.plate_controls_state = instance.text
        print("instance: {}, request update column={}, plate control={}".format(instance, self.disp_controls_state,
                                                                                self.plate_controls_state))

        # print("instance group {} {}".format(type(instance.group),instance.group))
        # raise Exception
        self.display_canvas.update_display(column=self.disp_controls_state, plate_control=self.plate_controls_state)

class ApplicationControls(GridLayout):
    def __init__(self, active_world, display_canvas, root, **kwargs):
        super(ApplicationControls, self).__init__(**kwargs)
        self.root=root
        self.active_world = active_world
        self.display_canvas = display_canvas
        self.cols = 1
        self.rows = 2

    def reset_world(self, world):
        self.active_world = world


class WorldDisplay(Widget):
    def __init__(self, active_world,column=None, plate_control=None, **kwargs):
        super(WorldDisplay, self).__init__(**kwargs)
        self.active_world = active_world
        self.display_type = self.active_world.conf.default_controls_state
        self.plate_type = self.active_world.conf.default_plates_state
        self.update_display(column=self.display_type, plate_control=self.plate_type)


        # self.current_world_pil = self.world_to_pil()
        # self.beeld = kiImage()  # only use this line in first code instance
        # self.pil_to_canvas()
        # self.beeld.texture = im.texture
        # with self.canvas:
        #     self.canvas_image = Rectangle(texture = self.beeld.texture, pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def reset_world(self, world):
        self.active_world = world

    def update_display(self, column, plate_control, force_update: bool = False):
        print("Update display column={}, plate control={}".format(column, plate_control))
        if column is None:
            column = self.display_type
            # raise Exception
        self.current_world_pil = self.world_to_pil(column=column,plate_control=plate_control, force_update=force_update)
        self.display_type = column
        self.pil_to_canvas()
        with self.canvas:
            self.canvas_image = Rectangle(texture=self.beeld.texture, pos=self.pos, size=self.size)

    def update_bg(self, *args):
        self.canvas_image.pos = self.pos
        self.canvas_image.size = self.size
        self.canvas_image.texture = self.beeld.texture

    def world_to_pil(self, column=None, plate_control=None, force_update: bool = False):
        print("world to pil column={}, plate control={}".format(column,plate_control))
        # print("root of widget {}".format(self.get_root_window()))
        # print("active world {}".format(self.active_world))
        if plate_control is 'plates_only':
            drawn = draw_plates(self.active_world, column=column, force_draw=force_update)
        elif plate_control is 'no_plates':
            drawn = draw_world(self.active_world, column=column, force_draw=force_update, hide_plates=True)
        else:
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


# class SplashScreen(Screen):
#     def __init__(self, active_world, root, **kwargs):
#         super(SplashScreen, self).__init__(**kwargs)
#         self.active_world = active_world
#         self.root = root
#         self.layout = SplashLayout(self.active_world, self.root)

class SplashLayout(RelativeLayout):
    def __init__(self, active_world, root, **kwargs):
        super(SplashLayout, self).__init__(**kwargs)
        self.active_world = active_world
        self.root = root
        self.main_options = GridLayout(cols=1, rows=2)
        self.add_widget(self.main_options)
        self.start_button = Button(text="start")
        self.start_button.bind(on_release=root.to_main_screen)
        self.settings_button = Button(text="settings")
        self.settings_button.bind(on_release=root.to_settings_screen)
        self.main_options.add_widget(self.start_button)
        self.main_options.add_widget(self.settings_button)

class SettingsLayout(GridLayout):
    def __init__(self, active_world, root, **kwargs):
        super(SettingsLayout, self).__init__(**kwargs)



        self.active_world = active_world
        self.root = root
        self.rows = 2
        self.cols = 1

        settings_buttons = {
            "World start size": {
                "Button": None,
                "Label": None,
                "Input": IntInput(),
                "Variable": self.active_world.conf.default_size
            }
        }

        self.settings_sub_layout = GridLayout(cols=3, rows=len(settings_buttons))
        self.add_widget(self.settings_sub_layout)

        self.input_to_variable = dict()

        for button_text, button_dict in settings_buttons.items():
            # if button_dict["Button"] is None:
            #     button_dict["Button"] = Button()
            #     button_dict["Button"].bind(on_press=)
            if button_dict["Label"] is None:
                button_dict["Label"] = Label(text=button_text)
            button_dict["Input"].bind(on_text_validate=self.on_enter)
            self.settings_sub_layout.add_widget(button_dict["Label"])
            # self.settings_sub_layout.add_widget(button_dict["Button"])
            self.settings_sub_layout.add_widget(button_dict["Input"])
            self.input_to_variable[button_dict["Input"]] = button_dict["Variable"]



        self.begin_button = Button(text="begin")
        self.begin_button.bind(on_release=root.to_main_screen)
        self.add_widget(self.begin_button)

    def on_enter(self, instance):
        self.input_to_variable[instance] = int(instance.text)
        print("settings buttons\n{}\nEnd settings buttons".format(self.active_world.conf.default_size))



# class MainScreen(Screen):
#     def __init__(self, active_world, root, **kwargs):
#         super(MainScreen, self).__init__(**kwargs)
#         self.active_world = active_world
#         self.root = root
#         self.layout = MainLayout(self.active_world, self.root)

class MainLayout(GridLayout):
    def __init__(self, active_world, root, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.active_world = active_world
        self.root = root
        self.cols = 2

        default_controls_state = active_world.conf.default_controls_state
        default_plates_state = active_world.conf.default_plates_state

        self.world_canvas = WorldDisplay( self.active_world)

        self.basic_controls = UserControls(self.active_world, self.world_canvas, root=self.root)
        self.basic_display_controls = UserDisplayControls(self.active_world, self.world_canvas)
        self.app_controls = ApplicationControls(self.active_world, self.world_canvas, root=self.root)


        self.add_widget(self.world_canvas)
        self.add_widget(self.basic_controls)
        self.add_widget(self.basic_display_controls)
        self.add_widget(self.app_controls)
        self.quit_button = Button(text="quit")
        self.quit_button.bind(on_release=self.quit_app)
        self.app_controls.add_widget(self.quit_button)
        self.reset_button = Button(text="New World")
        self.reset_button.bind(on_release=self.new_world)
        self.app_controls.add_widget(self.reset_button)

    def reset_world(self, world):
        self.active_world = world
        self.world_canvas = WorldDisplay(self.active_world)
        self.basic_controls.reset_world(self.active_world)
        self.basic_display_controls.reset_world(self.active_world)
        self.app_controls.reset_world(self.active_world)

    def quit_app(self, instance):
        App.get_running_app().stop()

    def new_world(self, instance):
        self.root.new_world()

class MapApp(App):
    def __init__(self, **kwargs):
        super(MapApp, self).__init__(**kwargs)
        self.active_world = World()
        self.active_conf = self.active_world.conf

    def new_world(self,world,instance=None,):
        print("application new world")
        self.active_world = world
        self.active_conf = self.active_world.conf

    def build(self):
        self.root = root = RootWidget(self.active_world, self)
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

    def __init__(self, active_world, application, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        self.application = application
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
        self.splash_screen = Screen(name="splash")
        self.splash_layout = SplashLayout(self.active_world, root=self)
        self.splash_screen.add_widget(self.splash_layout)
        self.main_screen = Screen(name="main")
        self.main_layout = MainLayout(self.active_world, root=self)
        self.main_screen.add_widget(self.main_layout)
        self.settings_screen = Screen(name="settings")
        self.settings_layout = SettingsLayout(self.active_world, root=self)
        self.settings_screen.add_widget(self.settings_layout)
        # self.main_screen = MainScreen(self.active_world, root=self, name="main")
        self.sm.add_widget(self.splash_screen)
        self.sm.add_widget(self.main_screen)
        print("sm curr {}".format(self.sm.current_screen))

    def new_world(self,instance=None):
        print("root new world")
        old_conf = self.active_world.conf
        self.active_world = World(old_conf)
        for child in self.children[:]:
            self.remove_widget(child)
        self.sm = ScreenManager()
        self.sm.transition = NoTransition()
        self.add_widget(self.sm)
        self.main_screen = Screen()
        self.main_layout = MainLayout(self.active_world, root=self)
        self.main_screen.add_widget(self.main_layout)
        self.sm.add_widget(self.main_screen)



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

    def to_main_screen(self, instance):
        self.sm.switch_to(self.main_screen)

    def to_settings_screen(self, instance):
        self.sm.switch_to(self.settings_screen)











if __name__ == '__main__':
    MapApp().run()