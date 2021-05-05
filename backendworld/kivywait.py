import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen,ScreenManager, NoTransition
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MainLayout,self).__init__(**kwargs)
        self.cols=2
        self.rows=2
        self.lbl1 = Label(text="hello")
        self.btn1 = Button(text="button")
        self.lbl2 = Label(text="hello")
        self.add_widget(self.lbl1)
        self.add_widget(self.btn1)
        self.add_widget(self.lbl2)
        self.wait_layout = WaitLayout()
        self.add_widget(self.wait_layout)
        self.wait_layout.size_hint=(1,1)
        # self.wait_layout.update_rect()
class WaitLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(WaitLayout, self).__init__(**kwargs)
        self.size_hint = (1,1)
        # self.make_rect()
        # self.wait_label = Label(text="Processing\nPlease wait", size_hint=(1,0.25),color=[1,0,0,1], font_size=50)
        # self.make_label()
        # self.wait_label.bind(pos=self.update_label)
        # self.wait_label.bind(size=self.update_label)
        # self.wait_label.texture_update()

        # self.add_widget(self.wait_label)
        self.world_canvas = WaitDisplay()

        self.add_widget(self.world_canvas)

        # self.update_rect()

    def make_label(self, *args):
        with self.wait_label.canvas.before:
            Color(0, 0, 0, 1)  # green; colors range from 0-1 instead of 0-255
            # self.rect = Rectangle(size=self.size,pos=self.pos)
            self.label_rect = Rectangle(size_hint=(1, 1))

    def update_label(self, *args):
        self.wait_label.size = self.size

    def start_circle(self):
        self.world_canvas.start_circle()

    def end_circle(self):
        self.world_canvas.end_circle()


    # def update_rect(self, *args):
    #     print("old waitlayout size {}, {}".format(self.size, self.pos))
    #
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size
    #     # self.canvas.clear()
    #
    #     print("waitlayout size {}, {}".format(self.size,self.pos))




class WaitDisplay(RelativeLayout):
    def __init__(self, **kwargs):
        super(WaitDisplay, self).__init__(**kwargs)
        self.make_rect()
        self.size_hint = (1,1)
        self.width = 400
        self.height=400
        self.canvas_image = None
        self.update_display()
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.position =0
        self.angle=9
        self.is_active = False
        self.wait_length = 0
        self.wait_timer = self.wait_length

    def make_rect(self, *args):
        with self.canvas.before:
            Color(0, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            # self.rect = Rectangle(size=self.size,pos=self.pos)
            self.rect = Rectangle(size_hint=(1,1))

    def update_rect(self, *args):
        # print("old waitlayout size {}, {}".format(self.size, self.pos))

        self.rect.pos = self.pos
        self.rect.size = self.size
        # self.canvas.clear()

        # print("waitlayout size {}, {}".format(self.size,self.pos))

    def update_display(self, *args):


        with self.canvas:
            Color(1, 0, 0)
            # self.canvas_image = Rectangle(pos =(10, 10), size =(self.width, self.height))
            # Line(circle=(150, 150, 50, 0, 360, 50)) #whole circle
            Clock.schedule_once(self._movecircle)
    def start_circle(self):
        self.is_active = True
        self._movecircle()

    def end_circle(self):
        self.is_active = False


    def _movecircle(self, *args):
        # print("movecircle size {}, {}".format(self.size, self.pos))
        self.canvas.clear()
        self.make_rect()
        with self.canvas:
            Color(1, 0, 0)
            x_pos = int(self.size[0]/2)
            y_pos = int(self.size[1] / 2)
            Line(circle=(x_pos, y_pos, int((3/4)*min(x_pos,y_pos)), self.position, self.position+self.angle, 50), width=3) #whole circle
            self.position=(self.position+self.angle)%360
            if self.is_active is True:
                self.wait_timer = self.wait_length
                Clock.schedule_once(self._movecircle)

    def _no_move(self, *args):
        if self.wait_timer <= 0:
            Clock.schedule_once(self._movecircle)
        else:
            self.wait_timer -= 1
            Clock.schedule_once(self._no_move)








class MapApp(App):
    # def __init__(self, **kwargs):
    #     super(MapApp, self).init(**kwargs)
    def build(self):
        return RootWidget()
class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget,self).__init__(**kwargs)
        self.sm = ScreenManager()
        self.sm.transition = NoTransition()
        self.add_widget(self.sm)
        self.main_screen = Screen()
        self.sm.add_widget(self.main_screen)
        self.main_layout = MainLayout()
        self.main_screen.add_widget(self.main_layout)



if __name__ == '__main__':
    MapApp().run()