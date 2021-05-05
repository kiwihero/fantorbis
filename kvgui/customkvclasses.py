from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import re

class ExtendedButton(BoxLayout):
    def __init__(self, main_button=None, dropdown_buttons=None, **kwargs):
        super(ExtendedButton, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        if main_button is None:
            self.main_button = Button()
        else:
            self.main_button = main_button
        self.dropdown_buttons = DropDown()
        self.expand_button = Button(text="More")
        self.expand_button.bind(on_release=self.dropdown_buttons.open)
        if dropdown_buttons is not None:
            for btn in [self.main_button]+dropdown_buttons:
                selector_button = Button(text=btn.text)
                selector_button.bind(on_release=lambda selector_button: self.dropdown_buttons.select(selector_button.text))
                self.dropdown_buttons.add_widget(selector_button)
        self.add_widget(self.main_button)
        self.add_widget(self.dropdown_buttons)

class IntInput(TextInput):
    pat = re.compile('[^0-9]')
    def __init__(self,**kwargs):
        super(IntInput, self).__init__(**kwargs)


    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        # if '.' in self.text:
        #     s = re.sub(pat, '', substring)
        # else:
        #     s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(IntInput, self).insert_text(s, from_undo=from_undo)