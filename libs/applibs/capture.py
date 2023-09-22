import os
import json
from datetime import datetime

import scapy.all as scapy
from kivymd.app import MDApp

class Capture():
    def __init__(self):
        self.packet_list = []
        self.app = MDApp.get_running_app()
        self.get_save_path()

    def get_save_path(self):
        with open(f'{self.app.user_data_dir}/configurations.json', 'r') as file:
            configurations = json.load(file)
        self.parent_dir = configurations["storage location"]
        self.parent_dir = os.path.expanduser(self.parent_dir)
        self.file_name = f'{datetime.now().strftime("%H-%M-%S-%d-%m-%Y")}.pcap'
        self.save_path = os.path.join(self.parent_dir, self.file_name)
        self.save_path = os.path.expanduser(self.save_path)
        self.store = configurations['store']

    def save_pcap(self):
        if self.store:
            try:
                scapy.wrpcap(self.save_path, self.packet_list)
            except FileNotFoundError:
                print(self.save_path)
                if not os.path.exists(self.parent_dir):
                    os.makedirs(self.parent_dir, exist_ok=True)
                with open(self.save_path, 'w') as pcap:
                    pass
                scapy.wrpcap(self.save_path, self.packet_list)


    def sniffer(self, iface):
        try:
            scapy.sniff(iface=iface, store=0, prn=self.process_packets)
        except PermissionError:
            print('ERROR: Not sufficient permissions to capture network interface')

    def process_packets(self, packet):
        if not self.app.is_running:
            raise KeyboardInterrupt('Sniffing Terminated')
        self.packet_list.append(packet)

    def get_cap_pkts(self):
        return self.packet_list

    def update_packet_list(self, ):
        return self.packet_list