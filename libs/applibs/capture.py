import sys
from io import StringIO

import scapy.all as scapy
from kivymd.app import MDApp


def sniffer(iface):
    scapy.sniff(iface=iface, store=False, prn=process_packets)

def process_packets(packet):
    print(packet)

def read_pcap(path):
    return scapy.rdpcap(path)

def get_hex(packet):
    hexdump = scapy.hexdump(packet, dump=True)
    dump_lines = format_lines(hexdump)
    return dump_lines

def get_packet_detail(packet):
    output = StringIO()
    sys.stdout = output
    packet.show()
    sys.stdout = sys.__stdout__
    details = output.getvalue()
    detail_lines = format_lines(details)
    return detail_lines

def format_lines(string):
    max_line_len = 71
    lines = string.splitlines()
    for line_no in range(len(lines)):
        if len(lines[line_no])>max_line_len:
            line = lines.pop(line_no)
            no_of_splitted_lines = 0
            for i in range(0, len(line), max_line_len):
                lines.insert(line_no + no_of_splitted_lines, line[i:i+max_line_len])
                no_of_splitted_lines += 1
    return lines

def filter_packets(packet_list, text):
    filtered_packet_list = []
    if text == '':
        return packet_list
    elif '=' in text and '.' in text:
        protocol, field, value = extract_filter_components(text)
        print(protocol, field, value)
        for packet in packet_list:
            if packet.haslayer(protocol) and field in packet[protocol].fields and str(packet[protocol].fields[field]) == value:
                filtered_packet_list.append(packet)
    else:
        for packet in packet_list:
            if packet.haslayer(text.upper()):
                filtered_packet_list.append(packet)
    return filtered_packet_list

def extract_filter_components(text):
    _filter, value = text.split('=')
    protocol, field = _filter.split('.')
    return protocol.upper(), field.lower(), value

def format_list_data(raw_packet_list):
    screen_manager = MDApp.get_running_app().root
    show_detail_fxn_obj = screen_manager.screen_instances['capturescreen'].show_detail
    formatted_packet_list = []
    for packet_number, packet in enumerate(raw_packet_list):
        if packet.haslayer('Ether'):
            if packet.haslayer('ARP'):
                list_item = {
                    'viewclass': 'ThreeLineListItem',
                    'text': f"{packet_number+1}. {packet['Ether'].src} -> {packet['Ether'].dst}",
                    'tertiary_text': f"    Protocal: ARP, Length: {len(packet)}"
                }
                if packet['ARP'].op == 'who-has':
                    list_item['secondary_text'] = f"    Who has {packet['ARP'].pdst}? Tell {packet['ARP'].psrc}"
                else:
                    list_item['secondary_text'] = f"    {packet['ARP'].psrc} is at {packet['ARP'].psrc}"
            elif packet.haslayer('IP'):
                if packet.haslayer('TCP'):
                    list_item = {
                        'viewclass': 'ThreeLineListItem',
                        'text': f"{packet_number+1}. {packet['IP'].src} -> {packet['IP'].dst}",
                        'secondary_text': f"    {packet['TCP'].sport} -> {packet['TCP'].dport}",
                        'tertiary_text': f"    Protocol: TCP, Length: {len(packet)}, Flags: {packet['TCP'].flags}"
                        }
                elif packet.haslayer('UDP'):
                    list_item = {
                        'viewclass': 'TwoLineListItem',
                        'text': f"{packet_number+1}. {packet['IP'].src} -> {packet['IP'].dst}",
                        'secondary_text': f"    {packet['UDP'].sport} -> {packet['UDP'].dport}",
                        'tertiary_text': f"    Protocol: UDP, Length: {len(packet)}"
                        }
                else:
                    list_item = {
                        'viewclass': 'TwoLineListItem',
                        'text': f"{packet_number+1}. {packet['IP'].src} -> {packet['IP'].dst}",
                        'secondary_text': f"    Length: {len(packet)}"
                        }

        elif packet.haslayer('Dot11'):
            list_item = {
                'viewclass': 'TwoLineListItem',
                'secondary_text': f"    Protocol: 802.11, Length: {len(packet)}, Type: {packet['Dot11'].type}, SubType: {packet['Dot11'].subtype}",
            }
            if 'addr2' in packet['Dot11'].fields:
                list_item['text'] = f"{packet_number+1}. {packet['Dot11'].addr2} -> {packet['Dot11'].addr1}"
            else:
                list_item['text'] = f"{packet_number+1}. Reciever Address: {packet['Dot11'].addr1}"
        else:
            print('packet has unidentified layer ')
            list_item = {
                'viewclass': 'OneLineListItem',
                'text': 'Unknown Layer2 Protocol'
            }
        list_item['on_release'] = lambda _packet=packet: show_detail_fxn_obj(_packet)
        formatted_packet_list.append(list_item)
    return formatted_packet_list