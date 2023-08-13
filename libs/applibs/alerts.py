import json

from kivymd.app import MDApp

import libs.applibs.conversation as cv

class Alert():
    def __init__(self):
        self.configuration = self.get_configuration()

    def get_configuration(self):
        with open(f'{MDApp.get_running_app().user_data_dir}/configurations.json', 'r') as file:
            configurations = json.load(file)
        return configurations

    def get_warnings(self, packet_list):
        warnings = []
        arp_scan_alerts = self.detect_arp_scan(packet_list, int(self.configuration['protocol baselines']['ARP Requests']))
        if arp_scan_alerts:
            for alert in arp_scan_alerts:
                warnings.append(alert)
        icmp_scan_alerts = self.detect_icmp_scan(packet_list, int(self.configuration['protocol baselines']['ICMP Echo Requests']))
        if icmp_scan_alerts:
            for alert in icmp_scan_alerts:
                warnings.append(alert)
        tcp_scan_alerts = self.detect_tcp_scan(packet_list, int(self.configuration['protocol baselines']['TCP SYN Requests']))
        if tcp_scan_alerts:
            for alert in tcp_scan_alerts:
                warnings.append(alert)
        bandwidth_alerts = self.check_for_bandwidth_baselines(packet_list, self.configuration['bandwidth baselines'])
        if bandwidth_alerts:
            for ip, bandwidth in bandwidth_alerts.items():
                warnings.append(('Bandwidth Alert', f'{ip} has exceeded its baseline bandwidth usage'))
        return warnings

    def get_critical_alerts(self, packet_list):
        critical_alerts = []
        duplicate_ip = self.detect_duplicate_ip(packet_list)
        duplicate_mac = self.detect_duplicate_mac(packet_list)
        if duplicate_ip:
            for ip, macs in duplicate_ip.items():
                critical_alerts.append(('ARP Poisioning Attack Detected', f'{ip} is used by {macs[0]} and {macs[1]}'))
        if duplicate_mac:
            for mac, ips in duplicate_mac.items():
                critical_alerts.append(('ARP Poisioning Attack Detected', f'{mac} is used by {ips[0]} and {ips[1]}'))
        return critical_alerts

    # warnings
    def check_for_bandwidth_baselines(self, packet_list, badwidth_baselines):
        bandwidth_alerts = {}
        conversations = cv.get_conversations(packet_list)
        conversations = cv.convert_units(conversations, 'MB')
        baselines = badwidth_baselines
        for ip, bandwidth in conversations.items():
            if baselines.get(ip):
                if bandwidth > int(baselines.get(ip)):
                    bandwidth_alerts[ip] = bandwidth
            else:
                if bandwidth > int(baselines.get('Default')):
                    bandwidth_alerts[ip] = bandwidth
        return bandwidth_alerts

    def detect_arp_scan(self, packet_list, arp_request_count):
        arp_requests = {}
        arp_replies = {}
        alerts = []
        for packet in packet_list:
            if packet.haslayer('ARP') and packet['ARP'].op==1:
                if arp_requests.get(packet['ARP'].psrc) == None:
                    arp_requests[packet['ARP'].psrc] = 1
                else:
                    arp_requests[packet['ARP'].psrc] += 1
            elif packet.haslayer('ARP') and packet['ARP'].op==2:
                if arp_replies.get(packet['ARP'].psrc) == None:
                    arp_replies[packet['ARP'].psrc] = 1
                else:
                    arp_replies[packet['ARP'].psrc] += 1
        for ip, count in arp_requests.items():
            if count > arp_request_count:
                alerts.append(('ARP Scan Detected', f'Unusual ARP Requests from {ip}'))
        for ip, count in arp_replies.items():
            if count > arp_request_count:
                alerts.append(('ARP Scan Detected', f'Unusual ARP Replies from {ip}'))
        return alerts

    def detect_icmp_scan(self, packet_list, icmp_request_count):
        icmp_echo_requests = {}
        alerts = []
        for packet in packet_list:
            if packet.haslayer('ICMP') and packet['ICMP'].type==8:
                if icmp_echo_requests.get(packet['IP'].src) == None:
                    icmp_echo_requests[packet['IP'].src] = 0
                else:
                    icmp_echo_requests[packet['IP'].src] += 1
        for ip, count in icmp_echo_requests.items():
            if count > icmp_request_count:
                alerts.append(('ICMP Scan Detected', f'Unusual ICMP Echo Replies from {ip}'))
        return alerts

    def detect_tcp_scan(self, packet_list, tcp_syn_count):
        tcp_syn = {}
        alerts = []
        for packet in packet_list:
            if packet.haslayer('TCP') and packet.haslayer('IP') and packet['TCP'].flags=='S':
                if tcp_syn.get(packet['IP'].src) == None:
                    tcp_syn[packet['IP'].src] = 0
                else:
                    tcp_syn[packet['IP'].src] += 1
        for ip, count in tcp_syn.items():
            if count > tcp_syn_count:
                alerts.append(('TCP SYN Scan Detected', f'Unusual TCP Syn packets from {ip}'))
        return alerts

    # critical alerts
    def detect_duplicate_mac(self, packet_list):
        mac_reply_map = {}
        duplicate_mac = {}
        for packet in packet_list:
            if packet.haslayer('ARP') and packet['ARP'].op==2:
                arp_reply = packet['ARP']
                previous_entry = mac_reply_map.get(arp_reply.hwsrc)
                if previous_entry == None:
                    mac_reply_map[arp_reply.hwsrc] = arp_reply.psrc
                elif arp_reply.psrc != previous_entry:
                    duplicate_mac[arp_reply.hwsrc] = [previous_entry, arp_reply.psrc]
        return duplicate_mac

    def detect_duplicate_ip(self, packet_list):
        ip_reply_map = {}
        duplicate_ip = {}
        for packet in packet_list:
            if packet.haslayer('ARP') and packet['ARP'].op==2:
                arp_reply = packet['ARP']
                previous_entry = ip_reply_map.get(arp_reply.psrc)
                if previous_entry == None:
                    ip_reply_map[arp_reply.psrc] = arp_reply.hwsrc
                elif arp_reply.hwsrc != previous_entry:
                    duplicate_ip[arp_reply.psrc] = [previous_entry, arp_reply.hwsrc]
        return duplicate_ip
