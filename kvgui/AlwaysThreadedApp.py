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
    def __init__(self, screen_manager, **kwargs):
        super(Thread, self).__init__(**kwargs)
        self.screen_manager = screen_manager
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
        print("done sleeping")
        self.screen_manager.proceed.disabled = False

        self.screen_manager.to_results()

    def First_thread(self, instance=None):

        self.screen_manager.proceed.disabled=True
        self.screen_manager.to_loading()
        t1 = threading.Thread(target=self.Slow_counter)
        t1.start()
        # threading.Thread(target=self.Slow_counter).start()
        # self.screen_manager.to_results()
        # time.sleep(5)
        # self.counter += 1
        # self.num_lbl.text = "{}".format(self.counter)

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManager, self).__init__(**kwargs)
        self.transition = NoTransition()
        thread1 = Thread(screen_manager=self)
        thread2 = BoxLayout()
        thread3 = BoxLayout()
        self.display_screen = DisplayScreen(name='display_screen',screen_manager=self)
        self.display_screen.add_widget(thread1)
        self.loading_screen = LoadingScreen(name='loading_screen',screen_manager=self)
        self.loading_screen.add_widget(thread2)
        self.results_screen = ResultsScreen(name='results_screen',screen_manager=self)
        self.results_screen.add_widget(thread3)
        self.add_widget(self.display_screen)
        self.add_widget(self.loading_screen)
        self.add_widget(self.results_screen)
        self.switch_to(self.display_screen)
        # print("current screen {}".format(self.current))
        next1 = Button(text="next screen: loading")
        next1.bind(on_release=self.to_loading)
        thread1.add_widget(next1)
        self.proceed = next2 = Button(text="next screen: results")
        next2.bind(on_release=self.to_results)
        thread2.add_widget(next2)
        next3 = Button(text="next screen: display")
        next3.bind(on_release=self.to_display)
        thread3.add_widget(next3)
        next3b = Label(text="Done")
        thread3.add_widget(next3b)
        # self.add_widget(self.loading_screen)
        # self.add_widget(self.results_screen)

    def to_display(self, instance=None):
        # print("to display")
        self.switch_to(self.display_screen)

    def to_loading(self, instance=None):
        # print("to loading")
        self.switch_to(self.loading_screen)

    def to_results(self, instance=None):
        # print("to results")
        self.switch_to(self.results_screen)

class DisplayScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(DisplayScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

class LoadingScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

class ResultsScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

class MyApp(App):
    def build(self):
        sm = ScreenManagement()
        return sm
        # return Thread()

if __name__ == "__main__":
    app = MyApp()
    app.run()
