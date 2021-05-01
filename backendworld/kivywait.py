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
class WaitLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(WaitLayout, self).__init__(**kwargs)
        self.world_canvas = WaitDisplay()
        self.add_widget(self.world_canvas)



class WaitDisplay(Widget):
    def __init__(self, **kwargs):
        super(WaitDisplay, self).__init__(**kwargs)
        self.width = 400
        self.height=400
        self.canvas_image = None
        self.update_display()
        self.position =0
        self.angle=90


    def update_display(self, *args):
        with self.canvas:
            Color(1, 0, 0)
            self.canvas_image = Rectangle(pos =(10, 10), size =(self.width, self.height))
            # Line(circle=(150, 150, 50, 0, 360, 50)) #whole circle
            Clock.schedule_once(self.movecircle,1)


    def movecircle(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0)
            Line(circle=(150, 150, 50, self.position, self.position+self.angle, 50)) #whole circle
            self.position=(self.position+self.angle)%360
            Clock.schedule_once(self.movecircle, 1)







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