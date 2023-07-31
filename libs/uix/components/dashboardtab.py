from functools import partial

from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import libs.applibs.plot as plt
from libs.applibs.networkinterface import NetworkInterface

Builder.load_file('libs/uix/kv/dashboardtab.kv')

class DashboardTab(MDTabsBase, MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.root = MDApp.get_running_app().root
        # self.capture = self.root.capture
        # self.capture_detail = self.capture.get_capture_detail()
        self.packet_list = []
    
    def load_pcap_dashboard(self, packet_list):
        self.packet_list = packet_list
        Clock.schedule_once(self.plot_bandwidth_fig)
        Clock.schedule_once(self.plot_conversation_fig)
        Clock.schedule_once(self.plot_protocol_chart)

    def plot_bandwidth_fig(self, t):
        pass

    def plot_conversation_fig(self, t):
        fig = plt.get_conversations_chart(self.packet_list, 4, 'KB')
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.conversations.clear_widgets(self.ids.conversations.children)
        self.ids.conversations.add_widget(canvas)

    def load_iface_dashboard(self, interface, capture_obj):
        interface_mac = NetworkInterface().get_iface_mac(interface)
        interface_ip = NetworkInterface().get_iface_ip(interface)
        Clock.schedule_interval(partial(self.update_packet_list, capture_obj), 2.5)
        Clock.schedule_interval(partial(self.plot_du_bandwidth_chart, interface_mac), 2.5)
        Clock.schedule_interval(self.plot_protocol_chart, 2.5)
        Clock.schedule_interval(partial(self.plot_du_conversation_chart, interface_ip), 2.5)

    def update_packet_list(self, capture_obj, t):
        self.packet_list = capture_obj.update_packet_list()

    def plot_du_bandwidth_chart(self, interface_mac, t):
        print('ploting bandwidth chart....')
        fig = plt.get_du_bandwidth_figure(self.packet_list, interface_mac)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.bandwidth_monitor.clear_widgets(self.ids.bandwidth_monitor.children)
        self.ids.bandwidth_monitor.add_widget(canvas)

    def plot_protocol_chart(self, t):
        print('updating protocol chart....')
        fig = plt.plot_protocol_chart(self.packet_list)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.protocol_chart.clear_widgets(self.ids.protocol_chart.children)
        self.ids.protocol_chart.add_widget(canvas)
    
    def plot_du_conversation_chart(self, interface_ip, t):
        print('updating conversation chart....')
        fig = plt.plot_du_conversations_chart(self.packet_list, 4, 'KB', interface_ip)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.conversations.clear_widgets(self.ids.conversations.children)
        self.ids.conversations.add_widget(canvas)



    