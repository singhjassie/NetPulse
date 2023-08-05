from math import ceil

def calculate_bandwidth(packets, interval):  # interval is used to reduce sharpen peeks of chart
    start_time = packets[0].time
    total_time = ceil(packets[-1].time - start_time)
    time_intervals = [t for t in range(1, total_time + 1, interval)]
    packet_number = 0
    bps = []
    for interval in time_intervals:
        bits = 0
        for packet in packets[packet_number:]:
            if packet.time < start_time + interval:
                bits += len(packet)
                packet_number += 1
            else:
                break
        bps.append(bits)
    return time_intervals, bps

def convert_units(bps, unit):
    values = []
    for b in bps:
        if unit=='bps':
            values.append(b)
        elif unit=='Kbps':
            values.append(b/1024)
        elif unit=='Mbps':
            values.append(b/1048576)
        elif unit=='Bps':
            values.append(b/8)
        elif unit=='KBps':
            values.append(b/8192)
        elif unit=='MBps':
            values.append(b/8388608)
        else:
            raise ValueError("Unit should be one of ['bps', 'Kbps', 'Mbps', 'Bps', 'KBps', 'MBps']")
    return values

def get_incoming_packets(packet_list, iface_mac):
    incoming_packets = []
    for packet in packet_list:
        if packet.haslayer('Ether') and packet['Ether'].dst == iface_mac:
            incoming_packets.append(packet)
    return incoming_packets

def get_outgoing_packets(packet_list, iface_mac):
    outgoing_packets = []
    for packet in packet_list:
        if packet.haslayer('Ether') and packet['Ether'].src == iface_mac:
            outgoing_packets.append(packet)
    return outgoing_packets

