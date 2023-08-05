# functions for interface dashboard
def get_du_conversations(packet_list, iface_ip):
    ips = set()
    for packet in packet_list:
        if packet.haslayer('IP'):
            ips.add(packet['IP'].src)
            ips.add(packet['IP'].dst)

    conversations = {}
    for ip in ips:
        conversations[ip] = [0, 0]
    if iface_ip in conversations.keys():
        del conversations[iface_ip]

    for packet in packet_list:
        if packet.haslayer('IP') and packet['IP'].src == iface_ip and conversations.get(packet['IP'].dst):
            conversations[packet['IP'].dst][0] += len(packet)
        if packet.haslayer('IP') and packet['IP'].dst == iface_ip and conversations.get(packet['IP'].src):
            conversations[packet['IP'].src][1] += len(packet)
    return conversations

def get_du_topn_conversations(packet_list, count, unit, iface_ip):
    conversations = get_du_conversations(packet_list, iface_ip)
    conversations = convert_du_units(conversations, unit)
    max_count = 8
    if count > max_count:
        count = max_count
    if len(conversations) < count:
        count = len(conversations)
    top_conversations = {}
    for i in range(count):
        max = [0, 0]
        max_ip = ''
        for ip, size in conversations.items():
            # print(ip, size)
            if sum(size) > sum(max):
                max = size
                max_ip = ip
        top_conversations[max_ip] = max
        conversations[max_ip] = 0, 0
    others = [0, 0]
    for count in conversations.values():
        others[0] += count[0]
        others[1] += count[1]
    top_conversations["Others"] = others
    return top_conversations

def convert_du_units(conversations, unit):
    for ip, size in conversations.items():
        if unit=='b':
            size[0] /= 1
            size[1] /= 1
        elif unit=='Kb':
            size[0] /= 1024
            size[1] /= 1024
        elif unit=='Mb':
            size[0] /= 1048576
            size[1] /= 1048576
        elif unit=='B':
            size[0] /= 8
            size[1] /= 8
        elif unit=='KB':
            size[0] /= 8192
            size[1] /= 8192
        elif unit=='MB':
            size[0] /= 8388608
            size[1] /= 8388608
        else:
            raise ValueError("Unit should be one of ['b', 'Kb', 'Mb', 'B', 'KB', 'MB']")
        conversations[ip] = size
    return conversations

def get_up_down_stat(conversations):
    upload_stat = []
    download_stat = []
    for upload, download in conversations.values():
        upload_stat.append(upload)
        download_stat.append(download)
    return upload_stat, download_stat




# functions for pcap dashboard

def get_conversations(packet_list):
    ips = set()
    for packet in packet_list:
        if packet.haslayer('IP'):
            ips.add(packet['IP'].src)
            ips.add(packet['IP'].dst)

    conversations = {}
    for ip in ips:
        conversations[ip] = 0

    for packet in packet_list:
        if packet.haslayer('IP'):
            conversations[packet['IP'].dst] += len(packet)
            conversations[packet['IP'].src] += len(packet)
    return conversations

def convert_units(conversations, unit):
    for ip, size in conversations.items():
        if unit=='b':
            size /= 1
        elif unit=='Kb':
            size /= 1024
        elif unit=='Mb':
            size /= 1048576
        elif unit=='B':
            size /= 8
        elif unit=='KB':
            size /= 8192
        elif unit=='MB':
            size /= 8388608
        else:
            raise ValueError("Unit should be one of ['b', 'Kb', 'Mb', 'B', 'KB', 'MB']")
        conversations[ip] = size
    return conversations


def get_topn_conversations(packet_list, count, unit):
    conversations = get_conversations(packet_list)
    conversations = convert_units(conversations, unit)
    max_count = 8
    if count > max_count:
        count = max_count
    if len(conversations) < count:
        count = len(conversations)
    top_conversations = {}
    for i in range(count):
        max = 0
        max_ip = ''
        for ip, size in conversations.items():
            # print(ip, size)
            if size > max:
                max = size
                max_ip = ip
        top_conversations[max_ip] = max
        conversations[max_ip] = 0
    others = 0
    for count in conversations.values():
        others += count
    top_conversations["Others"] = others
    return top_conversations