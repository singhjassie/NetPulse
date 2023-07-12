from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder

kv = """
<HomeScreen>:
    MDLabel:
        text: 'Hurray! i have made the home screen'
        halign: 'center'
"""

Builder.load_string(kv)

class HomeScreen(MDScreen):
    pass