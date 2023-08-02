from scapy.all import rdpcap, ARP, IP

def analyze_pcap(pcap_file, mac_address):
    packets = rdpcap(pcap_file)
    is_end_device = False
    is_router = False

    for packet in packets:
        if packet.haslayer(ARP):
            arp_packet = packet[ARP]
            if arp_packet.hwsrc == mac_address:
                is_end_device = True
            elif arp_packet.psrc != arp_packet.hwdst:
                is_router = True

    if is_end_device and not is_router:
        return "End Device"
    elif is_router and not is_end_device:
        return "Router"
    else:
        return "Unknown"

pcap_file = "evidence04.pcap"
mac_address = "00:12:79:45:a4:bb"

device_type = analyze_pcap(pcap_file, mac_address)
print(f"The device with MAC address {mac_address} is a {device_type}.")