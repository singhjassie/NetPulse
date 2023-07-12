from kivymd.app import MDApp
from kivy.core.window import Window

from libs.uix.baseclass.root import Root
from libs.uix.config import fonts

class NetPulse(MDApp):
    def __init__(self, **kwargs):
        super(NetPulse, self).__init__(**kwargs)
        Window.minimum_size = 1080, 720
        self.title = 'NetPulse'
        self.icon = 'assets/images/NetPulse-with-meterial-bg.png'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.font_styles.update(fonts.font_styles)
        print('hey')
        print(self.get_running_app().user_data_dir)

    def build(self):
        return Root()
