from kivymd.app import MDApp
from kivy.core.window import Window

from libs.uix.baseclass.root import Root
from libs.uix.config import fonts

class NetPulse(MDApp):
    def __init__(self, **kwargs):
        super(NetPulse, self).__init__(**kwargs)
        self.set_window_conf()
        self.set_theme_conf()
        self.set_app_conf()
        self.root = Root()
        self.is_running = True
        
    def set_app_conf(self):    
        self.title = 'NetPulse'
        self.icon = 'assets/images/NetPulse-with-meterial-bg.png'
        
    def set_window_conf(self):    
        Window.minimum_width = 950
        Window.minimum_height = 720
        Window.size = 1250, 750

    def set_theme_conf(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.font_styles.update(fonts.font_styles)

    def switch_theme(self):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'

        else:
            self.theme_cls.theme_style = 'Light'

    def on_stop(self):
        self.is_running =False
        try: 
            capture_obj = self.root.screen_instances['homescreen'].capture
        except AttributeError:
            capture_obj = None
        if capture_obj:
            capture_obj.save_pcap()
        try: 
            capture_thread = self.root.screen_instances['tabsscreen'].capture_thread
        except AttributeError:
            capture_thread = None
        if capture_thread:
            capture_thread.join()
        # current_process = mp.current_process()
        # current_process.terminate()
        return super().on_stop()
    
    def build(self):
        return self.root
    


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