import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


import libs.applibs.bandwidth as bw
import libs.applibs.protocol as protocol
import libs.applibs.conversation as cv

def plot_bandwidth_figure(u_time_intervals, upload_bandwidth, d_time_intervals, download_bandwidth,unit):
    fig, ax = plt.subplots()
    fig.set_figwidth(20)
    fig.set_figheight(5)
    ax.plot(u_time_intervals, upload_bandwidth,  label='Upload Speed', color='orange')
    ax.plot(d_time_intervals, download_bandwidth,  label='Download Speed', color='blue')

    def time_formatter(x, pos):
        minutes = int(x / 60) 
        return f'{minutes}'

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(time_formatter))

    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=1))

    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=60))

    ax.set_xlabel("Time (Minutes)")
    ax.set_ylabel(unit)
    fig.legend()
    # ax.set_title('Bandwidth')
    return fig

def get_du_bandwidth_figure(packet_list, iface_mac):
    if len(packet_list) > 0:
        download_bandwidth = [0]
        d_time_intervals = [0]
        upload_bandwidth = [0]
        u_time_intervals = [0]
        incoming_packets = bw.get_incoming_packets(packet_list, iface_mac)
        if len(incoming_packets)>0:
            d_time_intervals, download_bandwidth = bw.calculate_bandwidth(incoming_packets, 2)
        outgoing_packets = bw.get_outgoing_packets(packet_list, iface_mac)
        if len(outgoing_packets)>0:
            u_time_intervals, upload_bandwidth = bw.calculate_bandwidth(outgoing_packets, 2)
        if len(download_bandwidth) > 0 and len(upload_bandwidth) > 0:
            if max(download_bandwidth)/8<1024 and max(upload_bandwidth)/8<1024:
                unit = 'Bps'
            elif max(download_bandwidth)/8192<1024 and max(upload_bandwidth)/8192<1024:
                unit = 'KBps'
            else:
                unit = 'MBps'
            upload_bandwidth = bw.convert_units(upload_bandwidth, unit)
            download_bandwidth = bw.convert_units(download_bandwidth, unit)
            fig = plot_bandwidth_figure(u_time_intervals, upload_bandwidth, d_time_intervals, download_bandwidth, unit)
            return fig

def get_protocol_stat(packet_list):
    protocol_stat = protocol.get_protocol_stat(packet_list)
    return protocol_stat
    
def plot_protocol_chart(packet_list):
    fig, ax = plt.subplots()
    if len(packet_list) > 0:
        protocol_stat = get_protocol_stat(packet_list)
        ax.pie(protocol_stat.values(), labels=protocol_stat.keys(), autopct='%1.1f%%', labeldistance=1.2, colors=('green', 'orange', 'blue'))
        circle = plt.Circle((0, 0), 0.7, color='white')
        fig = plt.gcf()
        fig.gca().add_artist(circle)
        fig.legend()
    return fig

def plot_du_conversations_chart(packet_list, count, unit, iface_ip):
    top_conversations = cv.get_du_topn_conversations(packet_list, count, unit, iface_ip)
    upload_stat, download_stat = cv.get_up_down_stat(top_conversations)
    fig, ax = plt.subplots()
    ax.bar(top_conversations.keys(), upload_stat, color='orange', label='Upload')
    ax.bar(top_conversations.keys(), download_stat, color='blue', label='Download')
    plt.xticks(rotation=75)
    plt.ylabel(f'Data Transfered ({unit})')
    plt.legend()
    fig.tight_layout()
    return fig

def get_conversations_chart(packet_list, count, unit):
    top_conversations = cv.get_topn_conversations(packet_list, count, unit)
    fig, ax = plt.subplots()
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple']
    num_bars = len(top_conversations)
    colors = colors[0:num_bars]
    ax.bar(top_conversations.keys(), top_conversations.values(), color=colors)
    plt.xticks(rotation=75)
    plt.ylabel(f'Data Transfered ({unit})')
    plt.legend()
    fig.tight_layout()
    return fig