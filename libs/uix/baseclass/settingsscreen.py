from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

Builder.load_file('libs/uix/kv/settingsscreen.kv')

class SettingsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        