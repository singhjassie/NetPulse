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
        try:
            with open(f'{self.app.user_data_dir}/configurations.json', 'r') as file:
                configurations = json.load(file)
        except FileNotFoundError:
                self.create_default_configuration_file()
                with open(f'{self.app.user_data_dir}/configurations.json', 'r') as file:
                    configurations = json.load(file)
        self.parent_dir = configurations["storage location"]
        self.file_name = f'{datetime.now().strftime("%H-%M-%S-%d-%m-%Y")}.pcap'
        self.save_path = os.path.join(self.parent_dir, self.file_name)
        self.save_path = os.path.expanduser(self.save_path)
        self.store = configurations['store']

    def create_default_configuration_file(self):
        print("creating new config file......")
        with open(f'{self.app.user_data_dir}/configurations.json', 'w') as file:
            file.write("""{
                "store": "False",
                "storage location": "~/",
                "bandwidth baselines":{
                    "Default": 50
                },
                "protocol baselines":{
                    "ARP Requests": 10,
                    "ICMP Echo Requests": 10,
                    "TCP SYN Requests": 10
                },
                "colors": {
                    "TCP": "#4CAF50", 
                    "UDP": "#F44336", 
                    "ICMP": "#039BE5", 
                    "ARP": "#673AB7"}
            }""")

    def save_pcap(self):
        if self.store:
            try:
                scapy.wrpcap(self.save_path, self.packet_list)
            except FileNotFoundError:
                print(self.save_path)
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