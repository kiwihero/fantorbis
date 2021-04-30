from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from backendworld.World import World
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as kiImage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from PillowDisplay import draw_world, image_world

control_buttons = {'Move a random cell':None}

class UserControls(GridLayout):
    def __init__(self, active_world, **kwargs):
        super(UserControls, self).__init__(**kwargs)
        self.active_world = active_world
        self.cols = 1
        self.rows = 5

class WorldDisplay(Widget):
    def __init__(self, active_world, **kwargs):
        super(WorldDisplay, self).__init__(**kwargs)
        self.active_world = active_world
        self.world_to_canvas()
        # with self.canvas:

    def world_to_canvas(self):
        print("root of widget {}".format(self.get_root_window()))
        print("active world {}".format(self.active_world))
        created_dict = draw_world(self.active_world)
        canvas_img = created_dict[self.active_world.age]
        canvas_img.show()
        raise Exception

        # (do stuff to canvas_img)
        data = BytesIO()
        canvas_img.save(data, format='png')
        data.seek(0)  # yes you actually need this
        im = CoreImage(BytesIO(data.read()), ext='png')
        self.beeld = kiImage()  # only use this line in first code instance
        self.beeld.texture = im.texture

class MainScreen(GridLayout):
    def __init__(self, active_world, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.active_world = active_world

        self.cols = 2

        self.world_canvas = WorldDisplay(self.active_world)
        self.add_widget(self.world_canvas)
        # self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

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