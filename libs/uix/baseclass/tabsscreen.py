import json

from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivy.factory import Factory

Builder.load_file('libs/uix/kv/tabsscreen.kv')


class TabsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_tabs()
        self.add_tabs()

    def register_tabs(self):
        with open('factory_register.json', 'r') as fr:
            tabs = json.load(fr)
            for module, _classes in tabs.items():
                for _class in _classes:
                    Factory.register(_class, module=module)

    def add_tabs(self):
        self.capture_tab = Factory.CaptureTab()
        self.dashboard_tab = Factory.DashboardTab()
        # self.troubleshoot_tab = Factory.TroubleshootTab()
        self.preferences_tab = Factory.PreferencesTab()
        self.ids.tabs.add_widget(self.capture_tab)
        self.ids.tabs.add_widget(self.dashboard_tab)
        # self.ids.tabs.add_widget(self.troubleshoot_tab)
        self.ids.tabs.add_widget(self.preferences_tab)
