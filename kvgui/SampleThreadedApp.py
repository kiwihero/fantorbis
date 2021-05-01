from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.event import EventDispatcher
import logging
import multiprocessing
import time

class ThreadEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_thread_completion')
        super(ThreadEventDispatcher, self).__init__(**kwargs)

    def on_thread_completion(self, *args):
        print("Event dispatcher completion")
        pass

class ScreenMethodsMixin():
    def find_screen(self):
        curr = self
        print("Initial screen {}".format(curr))
        print(curr.parent)
        while type(curr) is not None and type(curr) is not ScreenManagement:
            curr = curr.parent
            print("New parent {}".format(curr))
        return curr

class ThreadedProgram():
    def __init__(self, dispatcher, **kwargs):
        super(ThreadedProgram, self).__init__(**kwargs)
        self.dispatcher = dispatcher
        # self.kill_requested = False
        self.quit = multiprocessing.Event()
        self.val = 0


    def sleep_program(self, sleep_time=1):
        self.kill_requested = False
        print("\nIN THREAD: STARTING PROGRAM\n")
        for x in range(2):
            print("x {}".format(x))
            self.val += 1
            time.sleep(sleep_time)
            if self.quit.is_set():
                return False
        print("\nIN THREAD: DONE WITH PROGRAM\n")
        return self.on_program_completion()

    def on_program_completion(self, *args):
        print("Program completed")
        self.dispatcher.dispatch('on_thread_completion', 'test_message')
        print("dispatcher sent")
        return True

class DisplayScreen(Screen):
    def __init__(self, **kwargs):
        super(DisplayScreen, self).__init__(**kwargs)
        self.layout = DisplayLayout()
        self.add_widget(self.layout)

class DisplayLayout(GridLayout,ScreenMethodsMixin):
    def __init__(self, **kwargs):
        super(DisplayLayout, self).__init__(**kwargs)
        self.rows=2
        self.cols=2
        self.start_button = Button(text="Start program")
        self.start_button.bind(on_release=self.start_threaded_program)
        self.add_widget(self.start_button)

    def start_threaded_program(self, instance):
        print("Starting program")
        sm = self.find_screen()
        sm.start_background()


        # print("Threaded program Screen manager {}".format(sm))
        # print("start_threaded_program thread {}".format(self.background_thread))
        # sm.switch_to(sm.known_screens["loading_screen"])
        # print("Current screen now {}".format(sm.current))
        # print("Starting background")
        # self.start_button.disabled = True
        # # background_dispatcher = sm.background_dispatcher
        #
        # print("Background thread commenced")
        # print("thread {} living? {}".format(sm.background_thread, sm.background_thread.is_alive()))
        # # self.background_thread.join()
        # # return background_dispatcher

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.layout = LoadingLayout()
        self.add_widget(self.layout)

class LoadingLayout(GridLayout,ScreenMethodsMixin):
    def __init__(self, **kwargs):
        super(LoadingLayout, self).__init__(**kwargs)
        self.rows = 2
        self.cols = 2
        self.start_label = Label(text="Running")
        self.add_widget(self.start_label)
        self.kill_button = Button(text="Kill program")
        self.kill_button.bind(on_release=self.kill_threaded_program)
        self.add_widget(self.kill_button)

    def kill_threaded_program(self, instance):
        print("Killing threaded program")
        sm = self.find_screen()
        sm.kill_background()
        print("thread {} living? {}".format(sm.background_thread, sm.background_thread.is_alive()))


    def update_progress(self, background_program=None):
        pass
        # sm = self.find_screen()
        # self.changing_label = Label(text=str(background_program.val))


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.layout = ResultsLayout()
        self.add_widget(self.layout)

class ResultsLayout(GridLayout,ScreenMethodsMixin):
    def __init__(self, **kwargs):
        super(ResultsLayout, self).__init__(**kwargs)
        self.rows=2
        self.cols=2
        self.next_screen_button = Button(text="Start another Program")
        self.next_screen_button.bind(on_release=self.goto_display_screen)
        self.add_widget(self.next_screen_button)

    def goto_display_screen(self, instance):
        sm = self.find_screen()

        sm.switch_to(sm.known_screens["display_screen"])

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManager, self).__init__(**kwargs)
        self.transition = NoTransition()
        self.display_screen = DisplayScreen(name='display_screen')
        self.loading_screen = LoadingScreen(name='loading_screen')
        self.results_screen = ResultsScreen(name='results_screen')
        self.add_widget(self.display_screen)
        self.add_widget(self.loading_screen)
        self.add_widget(self.results_screen)
        # self.initialize_screens()
        self.known_screens = {
            "display_screen": self.display_screen,
            "loading_screen": self.loading_screen,
            "results_screen": self.results_screen
        }
        self.switch_to(self.display_screen)

        self.ev = ev = ThreadEventDispatcher()
        ev.bind(on_thread_completion=self.background_completion)
        self.background_dispatcher = ThreadedProgram(self.ev)
        # self.background_thread = multiprocessing.Process(target=self.background_dispatcher.sleep_program)
        self.ui_thread = None
        self.background_thread = None


        # sm.background_thread =

    def start_background(self):
        print("Starting background thread")
        self.background_dispatcher = ThreadedProgram(self.ev)
        self.ui_thread = multiprocessing.Process(target=self.switch_to_loading)
        self.ui_thread.start()
        self.background_thread = multiprocessing.Process(target=self.background_dispatcher.sleep_program)
        self.background_thread.start()
        print("UI thread {}".format(self.ui_thread))
        print("Background thread {}".format(self.background_thread))
        # self.ui_thread.join()
        self.background_thread.join()
        print("Finished main")
        # raise Exception
        # self.known_screens["loading_screen"].layout.update_progress(self.background_dispatcher)
        # self.background_thread.start()


        # print("thread {} living? {}".format(self.background_thread, self.background_thread.is_alive()))

    def kill_background(self):
        print("Killing background thread")
        self.background_dispatcher.quit.set()
        # self.background_thread.terminate()
        print("thread {} living? {}".format(self.background_thread, self.background_thread.is_alive()))
        self.known_screens['display_screen'].layout.start_button.disabled = False
        print("SCREEN MANAGER HAS {}".format(self.screens))
        self.switch_to(self.display_screen)

    def background_completion(self, arg1, arg2):
        print("Background process complete screen arg1 {} arg2 {}".format(arg1,arg2))
        print("thread {} living? {}".format(self.background_thread, self.background_thread.is_alive()))
        # self.known_screens['display_screen'].layout.start_button.disabled = False
        # self.background_thread.join()
        print("SCREEN MANAGER HAS {}".format(self.screens))
        self.switch_to(self.results_screen)
        print("Screen manager current is now {}".format(self.current))

    # def initialize_screens(self):
    #     self.add_widget(self.display_screen)
    #     self.add_widget(self.loading_screen)
    #     self.add_widget(self.results_screen)

    def switch_to_loading(self):
        print("switch to loading screen")
        self.switch_to(self.loading_screen)
        self.loading_screen.layout.update_progress()
        print("current screen {}".format(self.current))
        print("done switching to loading")
        time.sleep(5)


class MapApp(App):
    def __init__(self, **kwargs):
        super(MapApp, self).__init__(**kwargs)

    def build(self):
        # multiprocessing.Process(target=self.background_dispatcher.sleep_program)
        sm = ScreenManagement()
        return sm


if __name__ == '__main__':
    MapApp().run()