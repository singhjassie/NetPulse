from kivymd.uix.navigationrail import MDNavigationRail
from kivy.lang.builder import Builder

Builder.load_string('''
<SideBar>:
    md_bg_color: app.theme_cls.bg_light
    MDNavigationRailItem:
        text: 'Home'
        icon: 'home'
    MDNavigationRailItem:
        text: 'DashBoard'
        icon: 'chart-bar'
    MDNavigationRailItem:
        text: 'Settings'
        icon: 'cog-outline'
    MDNavigationRailItem:
        text: 'Help'
        icon: 'help' ''')

class SideBar(MDNavigationRail):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)