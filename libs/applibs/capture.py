import scapy.all as scapy

class Capture():
    def __init__(self):
        self.packet_list = []
        # self.app = MDApp.get_running_app()
        # self.is_pcap = False
        # self.is_iface = False
        # self.selected_interface = None
        # self.selected_iface_mac = None
        # self.selected_iface_ip = None

    def sniffer(self, iface):
        # self.set_interface_detail(iface)
        try:
            scapy.sniff(iface=iface, store=False, prn=self.process_packets)
        except PermissionError:
            print('ERROR: Not sufficient permissions to capture network interface')

    def process_packets(self, packet):
        self.packet_list.append(packet)

    def get_cap_pkts(self):
        return self.packet_list

    def update_packet_list(self, ):
        print('updating packet list....')
        return self.packet_list

    
    # def read_pcap(self, path):
    #     # self.is_pcap = True
    #     self.packet_list = scapy.rdpcap(path)
    #     return self.packet_list
    
    # def get_iface_mac_ip(self, interface):
    #     return NetworkInterface().get_iface_mac_ip(interface)
    
    # def set_interface_detail(self, iface):
    #     self.selected_interface = iface
    #     self.selected_iface_mac, self.selected_iface_ip = NetworkInterface().get_iface_info(iface)

    # def get_capture_detail(self):
    #     details = {}
    #     if self.is_pcap:
    #         details['type'] = 'pcap'
    #         details['mac']  = None
    #         details['ip'] = None
    #     else:
    #         details['type'] = 'iface'
    #         details['mac'] = self.selected_iface_mac
    #         details['ip'] = self.selected_iface_ip
    #     return details