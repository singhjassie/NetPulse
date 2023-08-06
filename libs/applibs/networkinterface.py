import netifaces

class NetworkInterface():
    def __init__(self):
        self.interfaces = self.get_all_interfaces()

    def get_all_interfaces(self):
        interfaces = {}
        self.if_name_list = netifaces.interfaces()
        for iface in self.if_name_list:
            interface_info = {}
            iface_detail = netifaces.ifaddresses(iface)
            interface_info['mac_address'] = iface_detail[17][0]['addr']
            try:
                interface_info['ipv4_address'] = iface_detail[2][0]['addr']
            except KeyError:
                interface_info['ipv4_address'] = '-- Not Available --'
            try:
                interface_info['ipv4_netmask'] = iface_detail[2][0]['netmask']
            except KeyError:
                interface_info['ipv4_netmask'] = '-- Not Available --'
            try:
                interface_info['ipv6_address'] = iface_detail[10][0]['addr']
            except KeyError:
                interface_info['ipv6_address'] = '-- Not Available --'
            try:
                interface_info['ipv6_netmask'] = iface_detail[10][0]['netmask']
            except KeyError:
                interface_info['ipv6_netmask'] = '-- Not Available --'
            if self.is_wireless(iface):
                interface_info['type'] = 'wireless'
            elif self.is_localhost(interface_info['ipv4_address']):
                interface_info['type'] = 'localhost'
            elif self.is_ethernet(iface):
                interface_info['type'] = 'ethernet'
            else:
                interface_info['type'] = 'unknown'
            interfaces[iface] = interface_info
        return interfaces

    def is_wireless(self, iface):
        wireless_prefixes = ['wlan', 'wlp', 'ath', 'iwn', 'rtls', 'Wi-Fi',' Wireless Network Connection' ]
        for prefix in wireless_prefixes:
            if iface.startswith(prefix):
                return True
        return False
        
    def is_ethernet(self, iface):
        ethernet_prefixes = ['eth', 'en', 'em', 'bge', 'Ethernet']
        for prefix in ethernet_prefixes:
            if iface.startswith(prefix):
                return True
        return False

    def is_localhost(self, iface_ip):
        if iface_ip.startswith('127.'):
            return True
        
    def get_wireless_ifaces(self):
        wireless_interfaces = []
        for name, details in self.interfaces.items():
            if self.interfaces[name]['type'] == 'wireless':
                details['name'] = name
                wireless_interfaces.append(details)
        return wireless_interfaces
    
    def get_ethernet_ifaces(self):
        ethernet_interfaces = []
        for name, details in self.interfaces.items():
            if self.interfaces[name]['type'] == 'ethernet':
                details['name'] = name
                ethernet_interfaces.append(details)
        return ethernet_interfaces
    
    def get_localhost_ifaces(self):
        localhost_interfaces = []
        for name, details in self.interfaces.items():
            if self.interfaces[name]['type'] == 'localhost':
                details['name'] = name
                localhost_interfaces.append(details)
        return localhost_interfaces
    
    def get_other_ifaces(self):
        other_interfaces = []
        for name, details in self.interfaces.items():
            if self.interfaces[name]['type'] == 'unknown':
                details['name'] = name
                other_interfaces.append(details)
        return other_interfaces
    
    def get_iface_mac(self, iface):
        return self.interfaces[iface]['mac_address']
    
    def get_iface_ip(self, iface):
        return self.interfaces[iface]['ipv4_address']