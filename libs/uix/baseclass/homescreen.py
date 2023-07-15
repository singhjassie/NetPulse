from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

Builder.load_file('libs/uix/kv/homescreen.kv')

class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(HomeScreen, self).__init__(*args, **kwargs)