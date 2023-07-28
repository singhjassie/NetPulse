from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel

import libs.applibs.capture as capture


Builder.load_file('libs/uix/kv/capturescreen.kv')


class Tab(MDTabsBase, MDFloatLayout):
    pass


class CaptureScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_pcap = False
        self.is_interface_capture = False
        self.raw_packet_list = []
        self.formatted_packet_list = []

    def read_pcap(self, path, filename):
        print('reading pcap...')
        self.is_pcap = True
        self.raw_packet_list = capture.read_pcap(path)
        self.ids.capture_name.text = filename
        self.ids.packet_count.text = f"Total Packets: {len(self.raw_packet_list)}"
        print(f'pcap file has {len(self.raw_packet_list)} packets')
        self.formatted_packet_list = capture.format_list_data(self.raw_packet_list)
        self.show_detail(self.raw_packet_list[0])
        self.update_recycle_view(self.formatted_packet_list)

    def start_capture(self, interface):
        print(f'capturing on {interface}')
        self.is_interface_capture = True
        self.ids.capture_name.text = interface
        capture.sniffer(interface)
        

    def update_recycle_view(self, packet_list):
        self.ids.rv.data = packet_list

    def apply_filter(self, text):
        filtered_packet_list = capture.filter_packets(self.raw_packet_list, text)
        formatted_filtered_packet_list = capture.format_list_data(filtered_packet_list)
        self.update_recycle_view(formatted_filtered_packet_list)

    def show_detail(self, packet):
        self.ids.hex_box.clear_widgets(self.ids.hex_box.children)
        self.ids.detail_box.clear_widgets(self.ids.detail_box.children)
        dump_lines = capture.get_hex(packet)
        for line in dump_lines:
            self.ids.hex_box.add_widget(MDLabel(text=line, valign='top'))
        detail_lines = capture.get_packet_detail(packet)
        for line in detail_lines:
            self.ids.detail_box.add_widget(MDLabel(text=line, valign='top'))