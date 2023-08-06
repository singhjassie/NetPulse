import os
import json

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.snackbar import Snackbar
import scapy.all as scapy


from libs.applibs.networkinterface import NetworkInterface
from libs.applibs.capture import Capture


Builder.load_file('libs/uix/kv/homescreen.kv')

class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(HomeScreen, self).__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.screen_manager = self.app.root
        self.load_recent_pcap_list()
        self.set_interfaces()

    def set_interfaces(self):
        # set wireless interfaces
        self.wireless_menu = MDDropdownMenu()
        self.wireless_interfaces = NetworkInterface().get_wireless_ifaces()
        self.add_interfaces(self.wireless_interfaces, self.ids.wireless_drop_list, self.wireless_menu, self.ids.wireless_card_box)
        # set ethernet interfaces
        self.ethernet_menu = MDDropdownMenu()
        self.ethernet_interfaces = NetworkInterface().get_ethernet_ifaces()
        self.add_interfaces(self.ethernet_interfaces, self.ids.ethernet_drop_list, self.ethernet_menu, self.ids.ethernet_card_box)
        # set others interface
        self.others_menu = MDDropdownMenu()
        self.other_interfaces = NetworkInterface().get_localhost_ifaces()
        self.other_interfaces.extend(NetworkInterface().get_other_ifaces())
        self.add_interfaces(self.other_interfaces, self.ids.others_drop_list, self.others_menu, self.ids.others_card_box)

    def add_interfaces(self, interfaces, drop_list_id, menu, box_id):
        if len(interfaces) == 0:
            drop_list_id.text = 'None'
            box_id.add_widget(MDLabel(text='No Interface Available'))
        else:
            drop_list_id.text = interfaces[0]['name']
            self.add_details(box_id, interfaces[0])
            drop_list_id.current_item = interfaces[0]['name']
        menu_items = []
        for iface in interfaces:
            menu_items.append({'viewclass': 'OneLineListItem',
                               'text': iface['name'],
                               'on_release': lambda interface = iface : self.set_item(interface, drop_list_id, menu, box_id)})
        menu.caller = drop_list_id
        menu.items = menu_items
        menu.position = 'center'
        menu.width_mult = 3
        menu.bind()
        
    def set_item(self, interface, drop_list_id, menu, box_id):
        drop_list_id.set_item(interface['name'])
        for widget_id in list(box_id.ids.keys()):
            box_id.remove_widget(box_id.ids[widget_id])
        menu.dismiss()
        self.add_details(box_id, interface)

    def add_details(self, box_id, interface):
        mac_label = MDLabel(text=f'MAC: {interface["mac_address"]}', font_style= 'Subtitle2')
        ipv4_addr_label = MDLabel(text=f'IPv4 Addr: {interface["ipv4_address"]}', font_style= 'Subtitle2')
        ipv4_netmask_label = MDLabel(text=f'IPv4 Mask: {interface["ipv4_netmask"]}', font_style= 'Subtitle2')
        ipv6_addr_label = MDLabel(text=f'IPv6 Addr: {interface["ipv6_address"]}', font_style= 'Subtitle2')
        ipv6_netmask_label = MDLabel(text=f'IPv6 Mask: {interface["ipv6_netmask"]}', font_style= 'Subtitle2')
        box_id.add_widget(mac_label)
        box_id.ids[f'{interface["type"]}_mac'] = mac_label
        box_id.add_widget(ipv4_addr_label)
        box_id.ids[f'{interface["type"]}_ipv4_addr'] = ipv4_addr_label
        box_id.add_widget(ipv4_netmask_label)
        box_id.ids[f'{interface["type"]}_ipv4_mask'] = ipv4_netmask_label
        box_id.add_widget(ipv6_addr_label)
        box_id.ids[f'{interface["type"]}_ipv6_addr'] = ipv6_addr_label
        box_id.add_widget(ipv6_netmask_label)
        box_id.ids[f'{interface["type"]}_ipv6_mask'] = ipv6_netmask_label
        
    def load_recent_pcap_list(self):
        try:
            with open(f'{self.app.user_data_dir}/recent-pcaps.json', 'r') as recent_list_file:
                pcap_files = json.load(recent_list_file)
            for pcap in pcap_files:
                    self.ids.pcap_list.add_widget(
                        TwoLineListItem(
                            text=pcap['name'],
                            secondary_text=pcap['path'],
                            on_release=lambda x, path=pcap['path']: self.select_pcap(path))
                        )
        except FileNotFoundError:
            with open(f'{self.app.user_data_dir}/recent-pcaps.json', 'w') as recent_list_file:
                recent_list_file.write('[]')


    def open_file_manager(self):
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path,
            ext = ['.pcap', '.cap', '.dmp', '.pcapng']
        )
        self.file_manager.show(os.path.expanduser('~'))

    def exit_manager(self, *args):
        self.file_manager.close()
    
    def select_path(self, path):
        self.file_manager.close()
        self.select_pcap(path)
    
    def select_pcap(self, path):
        self.ids.selected_pcap_file.text=path

    def update_pcap_file(self, path):
        file_name = os.path.split(path)[1]
        user_home_dir = os.path.expanduser('~')
        if path.startswith(user_home_dir):
            path = path.replace(user_home_dir, '~')
        file_details = {"name": file_name, "path": path}
        with open(f'{self.app.user_data_dir}/recent-pcaps.json', 'r') as recent_pcap_files:
            pcap_files = json.load(recent_pcap_files)
        if file_details in pcap_files:
            pcap_files.remove(file_details)
        pcap_files.insert(0, file_details)
        if len(pcap_files)>5:
            pcap_files = pcap_files[0:5]
        json_data = json.dumps(pcap_files)
        with open(f'{self.app.user_data_dir}/recent-pcaps.json', 'w') as recent_pcap_files:
            recent_pcap_files.write(json_data)
    
    def open_settings(self):
        self.screen_manager.current = 'settingsscreen'

    def open_pcap(self, path):
        self.update_pcap_file(path)
        if path == '-- Not Selected --':
            pass
        else:
            path = os.path.expanduser(path)
            dir_path, filename = os.path.split(path)
            try:
                packet_list = scapy.rdpcap(path)
                self.tab_screen = self.screen_manager.screen_instances['tabsscreen']
                self.tab_screen.ids.capture_name.text = filename
                self.tab_screen.ids.packet_count.text = f'Total Packets: {len(packet_list)}'
                self.tab_screen.capture_tab.load_pcap_capture(packet_list, filename)
                self.tab_screen.dashboard_tab.load_pcap_dashboard(packet_list)
                self.screen_manager.current = 'tabsscreen'
            except FileNotFoundError:
                Snackbar(text = f'File {path} is removed!').open()

    def start_capture(self, interface):
        self.capture = Capture()
        self.tab_screen = self.screen_manager.screen_instances['tabsscreen']
        self.tab_screen.ids.capture_name.text = interface
        packet_counter = self.tab_screen.ids.packet_count
        self.tab_screen.capture_tab.start_capture(interface, self.capture, packet_counter)
        self.tab_screen.dashboard_tab.load_iface_dashboard(interface, self.capture)
        self.screen_manager.current = 'tabsscreen'
        
