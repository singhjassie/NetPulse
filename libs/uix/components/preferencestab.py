from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang.builder import Builder

Builder.load_file('libs/uix/kv/preferencestab.kv')

class PreferencesTab(MDTabsBase, MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)