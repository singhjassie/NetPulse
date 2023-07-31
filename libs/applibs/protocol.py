def get_protocol_stat(packet_list):
    protocol_stat = {'TCP': 0, 'UDP': 0, 'Others': 0}
    for packet in packet_list:
        if packet.haslayer('TCP'):
            protocol_stat['TCP'] += 1
        elif packet.haslayer('UDP'):
            protocol_stat['UDP'] += 1
        else:
            protocol_stat['Others'] += 1
    return protocol_stat