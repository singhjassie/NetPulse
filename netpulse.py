from kivymd.app import MDApp
from kivy.core.window import Window

from libs.uix.baseclass.root import Root
from libs.uix.config import fonts

class NetPulse(MDApp):
    def __init__(self, **kwargs):
        super(NetPulse, self).__init__(**kwargs)
        Window.minimum_width = 1080
        Window.minimum_height = 720
        Window.size = 1440, 810
        self.title = 'NetPulse'
        self.icon = 'assets/images/NetPulse-with-meterial-bg.png'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.font_styles.update(fonts.font_styles)

    def switch_theme(self):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'

        else:
            self.theme_cls.theme_style = 'Light'

    def build(self):
        return Root()
    


# HOTRELOAD CODE

# from kivymd.tools.hotreload.app import MDApp
# from kivy.core.window import Window

# from libs.uix.baseclass.root import Root
# from libs.uix.config import fonts

# class NetPulse(MDApp):
#     DEBUG = True
#     KV_FILES = ['libs/uix/kv/homescreen.kv']
#     def __init__(self, **kwargs):
#         super(NetPulse, self).__init__(**kwargs)
#         Window.minimum_width = 1080
#         Window.minimum_height = 720
#         Window.size = 1440, 810
#         self.title = 'NetPulse'
#         self.icon = 'assets/images/NetPulse-with-meterial-bg.png'
#         self.theme_cls.theme_style = 'Light'
#         self.theme_cls.theme_style_switch_animation = True
#         self.theme_cls.primary_palette = 'Red'
#         self.theme_cls.font_styles.update(fonts.font_styles)

#     def switch_theme(self):
#         if self.theme_cls.theme_style == 'Light':
#             self.theme_cls.theme_style = 'Dark'  
#         else:
#             self.theme_cls.theme_style = 'Light'

#     def build_app(self):
#         return Root()