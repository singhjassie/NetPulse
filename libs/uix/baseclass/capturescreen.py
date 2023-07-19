from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

Builder.load_file('libs/uix/kv/capturescreen.kv')

class CaptureScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        