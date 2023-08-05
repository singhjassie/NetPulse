import os
import json
from typing import Union


from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDColorPicker

Builder.load_file('libs/uix/kv/preferencestab.kv')

class PreferencesTab(MDTabsBase, MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.configurations = {}
        self.baseline_widgets = []
        self.load_user_configration()

    def load_user_configration(self):
        try:
            with open(f'{self.app.user_data_dir}/configurations.json', 'r') as file:
                self.configurations = json.load(file)
        except FileNotFoundError:
            self.load_defaults()
        self.update_tab()

    def update_tab(self):
        self.ids.auto_capture_switch.active = self.configurations['store']
        self.ids.file_path.text = self.configurations['storage location']
        self.ids.baseline_rules.clear_widgets(self.ids.baseline_rules.children)
        for ip, baseline in self.configurations['baselines'].items():
            self.add_bandwidth_rule(ip, baseline)
        self.ids.tcp_color.text_color = self.configurations['colors']['TCP']
        self.ids.udp_color.text_color = self.configurations['colors']['UDP']
        self.ids.icmp_color.text_color = self.configurations['colors']['ICMP']
        self.ids.arp_color.text_color = self.configurations['colors']['ARP']
            

    def load_defaults(self):
        try:
            with open('configurations.json', 'r') as file:
                self.configurations = json.load(file)
        except FileNotFoundError:
            self.create_default_configuration_file()
            with open('configurations.json', 'r') as file:
                self.configurations = json.load(file)
        json_data = json.dumps(self.configurations)
        with open(f'{self.app.user_data_dir}/configurations.json', 'w') as file:
            file.write(json_data)
        self.update_tab()

    def open_color_picker(self, protocol):
        self.color_picker = MDColorPicker(size_hint=(0.45, 0.85), type_color='HEX', background_down_button_selected_type_color = [1,1,1,1])
        self.color_picker.open()
        self.color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=lambda instance_color_picker, type_color, selected_color, protocol=protocol: self.get_selected_color(protocol, selected_color)
        )
    
    def on_select_color(self, instance_gradient_tab, color: list):
        pass

    def get_selected_color(self, protocol, selected_color):
        # print(f"Selected color is {selected_color}")
        # print(f'protocol: {protocol}')
        self.color_picker.dismiss()
        hex_color = self.rgba_to_hex(selected_color)
        self.configurations['colors'][protocol] = hex_color
        self.update_tab()
        # print(f"Selected color is {hex_color}")

    def rgba_to_hex(obj, rgba):
        # print(rgba)
        # print(obj)
        r, g, b, a = rgba
        return "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))


    def open_file_manager(self):
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path
        )
        self.file_manager.show(os.path.expanduser('~'))
    
    def select_path(self, path):
        self.file_manager.close()
        self.ids.file_path.text = path

    def exit_manager(self, *args):
        self.file_manager.close()

    def apply_changes(self):
        configurations = {
            'store': self.ids.auto_capture_switch.active,
            'storage location': self.ids.file_path.text,
            'baselines': self.configurations['baselines'],
            'colors': self.configurations['colors']
        }
        configurations_str = json.dumps(configurations)
        with open(f'{self.app.user_data_dir}/configurations.json', 'w') as file:
            file.write(configurations_str)


    def add_bandwidth_rule(self, ip, bandwidth):
        self.configurations['baselines'][ip] = bandwidth
        bandwidth_rule = BandwidthRule(ip=ip, bandwidth=str(bandwidth), remove_fxn_obj=self.remove_bandwidth_rule)
        self.baseline_widgets.append(bandwidth_rule)
        self.ids.baseline_rules.add_widget(bandwidth_rule)

    def remove_bandwidth_rule(self, rule_widget):
        self.ids.baseline_rules.remove_widget(rule_widget)
    
    def add_bandwidth_callback(self, ip, bandwidth):
        self.add_bandwidth_rule(ip, bandwidth)
        self.dialog.dismiss()

    def open_dialog(self):
        self.dialog=MDDialog(
            content_cls = AddRuleDialog(add_fxn_obj = self.add_bandwidth_callback),
            type = 'custom'
        )
        self.dialog.open()

    def create_default_configuration_file(self):
        with open('configurations.json', 'w') as file:
            file.write({
                "store": "False",
                "storage location": "~/",
                "baselines":{
                    "default": 50
                },
                "colors": {
                    "TCP": "#4CAF50", 
                    "UDP": "#F44336", 
                    "ICMP": "#039BE5", 
                    "ARP": "#673AB7"}
            })

class BandwidthRule(MDBoxLayout):
    def __init__(self, remove_fxn_obj, ip='', bandwidth = '', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'horizontal'
        self.spacing = 50
        self.ip = ip
        self.bandwidth = bandwidth
        rule_widget = self
        self.add_widget(MDTextField(hint_text='IP Address', text=self.ip))
        self.add_widget(MDTextField(hint_text='Bandwidth (in mB)', text=f'{self.bandwidth} MB'))
        self.add_widget(MDIconButton(icon='trash-can-outline', on_release=lambda instance: remove_fxn_obj(rule_widget)))

class AddRuleDialog(MDBoxLayout):
    def __init__(self, add_fxn_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_fxn_obj = add_fxn_obj