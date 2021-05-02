from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.event import EventDispatcher
import logging
import multiprocessing
import threading
import time
from kivy.properties import NumericProperty


class Thread(BoxLayout):
    def __init__(self, **kwargs):
        super(Thread, self).__init__(**kwargs)
        self.counter = counter = 0
        self.thread_button = use_button = Button(text="use thread")
        use_button.bind(on_release=self.First_thread)
        self.add_widget(use_button)
        hit_button = Button(text="hit me")
        hit_button.bind(on_release=self.Counter_function)
        self.add_widget(hit_button)
        self.num_lbl = number_label = Label(text="numbers")
        self.add_widget(number_label)
        # self.load_kv('thread.kv')

    def Counter_function(self, instance=None):
        self.counter += 1
        self.num_lbl.text = "{}".format(self.counter)

    def Slow_counter(self, instance=None):
        self.thread_button.disabled=True
        time.sleep(5)
        self.counter += 1
        self.num_lbl.text = "{}".format(self.counter)
        self.thread_button.disabled=False

    def First_thread(self, instance=None):
        threading.Thread(target=self.Slow_counter).start()
        # time.sleep(5)
        # self.counter += 1
        # self.num_lbl.text = "{}".format(self.counter)

class MyApp(App):
    def build(self):
        return Thread()

if __name__ == "__main__":
    app = MyApp()
    app.run()
