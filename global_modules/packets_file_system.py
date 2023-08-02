from io import BytesIO
from mac_vendor_lookup import MacLookup
from scapy.all import *
from scapy.layers.inet import IP
from issues import network
from issues.connection import Connection
from issues.device import Device


def proto_name_by_num(proto_num):
    for name, num in vars(socket).items():
        if name.startswith("IPPROTO") and proto_num == num:
            return name[8:]
    return "Protocol not found"


def file_integrity_check(file):
    split_tup = os.path.splitext(file)
    file_extension = split_tup[1]
    if file_extension == ".pcap":
        return True
    # TODO remember the cap,pcapng
    return False


def check_file(file):
    if file_integrity_check(file) is False:
        return False
    return True


def get_mac_address(packet):
    src_mac = packet["Ether"].src
    dst_mac = packet["Ether"].dst
    return src_mac, dst_mac


def get_vendor(mac_address):
    return MacLookup().lookup(mac_address)


async def get_device(mac_address):
    vendor = "some_vendor."
    network_id = network.current_network.network_id
    device = Device(vendor=vendor, mac_address=mac_address, network_id=network_id)
    return device


def get_protocol(packet):
    protocol = proto_name_by_num(int(packet[IP].proto))
    return protocol


async def open_pcap_file(pcap_file):
    file_content = BytesIO(await pcap_file.read())
    packets = rdpcap(file_content)
    return packets


def check_protocol_exist(connections_lst, protocol):
    for connection in connections_lst:
        if protocol == connection.protocol:
            return True

    return False


async def get_devices_to_add(pcap_file):
    devices = {}
    packets = await open_pcap_file(pcap_file)
    for packet in packets:
        if packet.haslayer("Ether"):
            src_mac, dst_mac = get_mac_address(packet)
            if packet.haslayer("IP"):
                protocol = get_protocol(packet)
            connection = Connection(src_mac_address=src_mac, dst_mac_address=dst_mac, protocol=protocol)
            if not devices.get(src_mac):
                src_device = await get_device(src_mac)
                devices[src_mac] = {"device": src_device,
                                    "connections": []}

            if connection not in devices[src_mac]["connections"]:
                devices[src_mac]["connections"].append(connection)
            elif not check_protocol_exist(devices[src_mac]["connections"], connection.protocol):
                devices[src_mac]["connections"].append(connection)

            if not devices.get(dst_mac):
                dst_device = await get_device(dst_mac)
                devices[dst_mac] = {"device": dst_device,
                                    "connections": []}

    return dict(devices)
