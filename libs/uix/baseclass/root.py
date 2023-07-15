import json

from kivy.clock import Clock
from kivy.factory import Factory
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder

Builder.load_file('libs/uix/kv/root.kv')

class Root(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        self.add_screens()
        print(self.ids.screen_manager.screens)
        self.ids.screen_manager.current = 'Home'
        self.ids.top_bar.title = 'Home'

    def add_screens(self):
        with open('screens.json', 'r') as screens_file:
            screens = json.load(screens_file)
            for import_screen_module, screen_details in screens.items():
                exec(import_screen_module)
                screen_object = eval(screen_details["factory"])
                screen_object.name = screen_details["screen_name"]
                self.ids.screen_manager.add_widget(screen_object)
