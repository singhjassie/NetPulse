from threading import Thread
from multiprocessing import Process
from functools import partial

from kivy.clock import Clock
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivy.lang.builder import Builder

import libs.applibs.dataformatting as df 

Builder.load_file('libs/uix/kv/capturetab.kv')

class CaptureTab(MDTabsBase, MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_packet_list = []
        self.formatted_packet_list = []
        self.store = False

    def load_pcap_capture(self, packet_list, filename):
        # self.is_pcap = True
        self.raw_packet_list = packet_list
        self.formatted_packet_list = df.format_list_data(self.raw_packet_list)
        self.show_detail(self.raw_packet_list[0])
        self.update_recycle_view(self.formatted_packet_list)

    def start_capture(self, interface, capture_obj, packet_counter):
        # print(f'starting capture on {interface}')
        # self.is_interface_capture = True
        self.capture_thread = Thread(target=capture_obj.sniffer, args=[interface])
        self.capture_thread.start()
        Clock.schedule_interval(partial(self.update_packets, capture_obj, packet_counter), 1)

    def update_packets(self, capture_obj, packet_counter, interval):
        self.raw_packet_list = capture_obj.get_cap_pkts()
        self.formatted_packet_list = df.format_list_data(self.raw_packet_list)
        packet_counter.text = f'Total Packets: {str(len(self.formatted_packet_list))}'
        # self.ids.rv.scroll_y = 0
        self.update_recycle_view(self.formatted_packet_list)

    def update_recycle_view(self, packet_list):
        self.ids.rv.data = packet_list

    def apply_filter(self, text):
        filtered_packet_list = df.filter_packets(self.raw_packet_list, text)
        formatted_filtered_packet_list = df.format_list_data(filtered_packet_list)
        self.update_recycle_view(formatted_filtered_packet_list)

    def show_detail(self, packet):
        self.ids.hex_box.clear_widgets(self.ids.hex_box.children)
        self.ids.detail_box.clear_widgets(self.ids.detail_box.children)
        dump_lines = df.get_hex(packet)
        for line in dump_lines:
            self.ids.hex_box.add_widget(MDLabel(text=line, valign='top'))
        detail_lines = df.get_packet_detail(packet)
        for line in detail_lines:
            self.ids.detail_box.add_widget(MDLabel(text=line, valign='top'))
        