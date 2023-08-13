from functools import partial

from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
# from kivymd.uix.list import TwoLineIconListItem

import libs.applibs.plot as plt
from libs.applibs.networkinterface import NetworkInterface
from libs.applibs.alerts import Alert

Builder.load_file('libs/uix/kv/dashboardtab.kv')

class DashboardTab(MDTabsBase, MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.packet_list = []
        self.alert_obj = Alert()
        self.warnings = []
        self.critical_alerts = []
        self.interface = None

    def load_iface_dashboard(self, interface, capture_obj):
        self.interface = interface
        interface_mac = NetworkInterface().get_iface_mac(interface)
        interface_ip = NetworkInterface().get_iface_ip(interface)
        Clock.schedule_interval(partial(self.update_packet_list, capture_obj), 2.5)
        Clock.schedule_interval(partial(self.plot_du_bandwidth_chart, interface_mac), 2.5)
        Clock.schedule_interval(self.plot_protocol_chart, 2.5)
        Clock.schedule_interval(partial(self.plot_du_conversation_chart, interface_ip), 2.5)
        Clock.schedule_interval(self.detect_alerts, 2.5)
    
    def load_pcap_dashboard(self, packet_list):
        self.packet_list = packet_list
        Clock.schedule_once(self.plot_total_bandwidth_fig)
        Clock.schedule_once(self.plot_conversation_fig)
        Clock.schedule_once(self.plot_protocol_chart)
        Clock.schedule_once(self.detect_alerts)

    def plot_total_bandwidth_fig(self, t):
        fig = plt.get_total_bandwidth_fig(self.packet_list)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.bandwidth_monitor.clear_widgets(self.ids.bandwidth_monitor.children)
        self.ids.bandwidth_monitor.add_widget(canvas)

    def plot_conversation_fig(self, t):
        fig = plt.get_conversations_chart(self.packet_list, 4, 'KB')
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.conversations.clear_widgets(self.ids.conversations.children)
        self.ids.conversations.add_widget(canvas)


    def update_packet_list(self, capture_obj, t):
        self.packet_list = capture_obj.update_packet_list()

    def plot_du_bandwidth_chart(self, interface_mac, t):
        # print('ploting bandwidth chart....')
        fig = plt.get_du_bandwidth_figure(self.packet_list, interface_mac)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.bandwidth_monitor.clear_widgets(self.ids.bandwidth_monitor.children)
        self.ids.bandwidth_monitor.add_widget(canvas)

    def plot_protocol_chart(self, t):
        # print('updating protocol chart....')
        fig = plt.plot_protocol_chart(self.packet_list)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.protocol_chart.clear_widgets(self.ids.protocol_chart.children)
        self.ids.protocol_chart.add_widget(canvas)
    
    def plot_du_conversation_chart(self, interface_ip, t):
        # print('updating conversation chart....')
        fig = plt.plot_du_conversations_chart(self.packet_list, 4, 'KB', interface_ip)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.conversations.clear_widgets(self.ids.conversations.children)
        self.ids.conversations.add_widget(canvas)

    def detect_alerts(self, t):
        warnings = self.alert_obj.get_warnings(self.packet_list)
        critical_alerts = self.alert_obj.get_critical_alerts(self.packet_list)
        if warnings:
            self.warnings = warnings
            self.update_alerts()
        if critical_alerts:
            self.critical_alerts = critical_alerts
            self.update_alerts()

    def update_alerts(self):
        alerts = []
        fig = plt.get_alert_chart(self.warnings, self.critical_alerts)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.alert_chart.clear_widgets(self.ids.alert_chart.children)
        self.ids.alert_chart.add_widget(canvas)
        self.ids.alert_count.clear_widgets(self.ids.alert_count.children)
        self.ids.alert_count.add_widget(MDLabel(text=f'Critical Alerts: {len(self.critical_alerts)}',
                                                theme_text_color= 'Custom',
                                                text_color = 'red',
                                                halign='center'))
        self.ids.alert_count.add_widget(MDLabel(text=f'Warnings: {len(self.warnings)}',
                                                theme_text_color= 'Custom',
                                                text_color = 'orange',
                                                halign='center'))
        for critical_alert in self.critical_alerts:
            alerts.append({
                'viewclass': 'TwoLineListItem',
                'text': f'{critical_alert[0]}',
                'secondary_text': f'{critical_alert[1]}',
                'theme_text_color': 'Error'
            })
        for warning in self.warnings:
            print(warning)
            alerts.append({
                'viewclass': 'TwoLineListItem',
                'text': warning[0],
                'secondary_text': warning[1],
                'theme_text_color': 'Custom',
                'text_color': 'orange'
            })
        self.ids.rv.data = alerts

    