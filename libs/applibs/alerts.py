import json

from kivymd.app import MDApp

import libs.applibs.conversation as cv

def get_warnings(packet_list):
    warnings = []
    bandwidth_alerts = check_for_bandwidth_baselines(packet_list)
    if bandwidth_alerts:
        for ip, bandwidth in bandwidth_alerts.items():
            warnings.append(f'{ip} has exceeded its baseline bandwidth usage')
    return warnings

def get_critical_alerts(packet_list):
    critical_alerts = []
    duplicate_ip = detect_duplicate_ip(packet_list)
    duplicate_mac = detect_duplicate_mac(packet_list)
    if duplicate_ip:
        for ip, macs in duplicate_ip.items():
            critical_alerts.append(('ARP Poisioning Attack Detected', f'{ip} is used by {macs[0]} and {macs[1]}'))
    if duplicate_mac:
        for mac, ips in duplicate_mac.items():
            critical_alerts.append(('ARP Poisioning Attack Detected', f'{mac} is used by {ips[0]} and {ips[1]}'))
    return critical_alerts

# warnings
def get_baselines():
    with open(f'{MDApp.get_running_app().user_data_dir}/configurations.json', 'r') as file:
        configurations = json.load(file)
    return configurations['baselines']

def check_for_bandwidth_baselines(packet_list):
    bandwidth_alerts = {}
    conversations = cv.get_conversations(packet_list)
    conversations = cv.convert_units(conversations, 'MB')
    baselines = get_baselines()
    for ip, bandwidth in conversations.items():
        if baselines.get(ip):
            if bandwidth > int(baselines.get(ip)):
                bandwidth_alerts[ip] = bandwidth
        else:
            if bandwidth > int(baselines.get('default')):
                bandwidth_alerts[ip] = bandwidth
    return bandwidth_alerts

            

# critical alerts
def detect_duplicate_mac(packet_list):
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

def detect_duplicate_ip(packet_list):
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
