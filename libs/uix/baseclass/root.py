import json

from kivy.clock import Clock
from kivy.factory import Factory
from kivymd.uix.screenmanager import MDScreenManager

class Root(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.add_screens)

    def add_screens(self, interval):
        with open('screens.json', 'r') as screens_file:
            screens = json.load(screens_file)
            for import_screen_module, screen_details in screens.items():
                exec(import_screen_module)
                screen_object = eval(screen_details['factory'])
                screen_object.name = screen_details['screen_name']
                self.add_widget(screen_object)
