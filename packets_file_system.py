import os
from pathlib import Path
import socket

from mac_vendor_lookup import MacLookup
from scapy.all import *
from scapy.layers.inet import IP, Ether
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6

from issuies import network
from issuies.connection import Connection
from issuies.device import Device
from issuies.network import NetworkInDB


# list_protocol = []
# list_mac_dst = []
# list_mac_src = []
# list_IP_dst = []
# list_IP_src = []


# find the protocol name from number that getting
def proto_name_by_num(proto_num):
    for name, num in vars(socket).items():
        if name.startswith("IPPROTO") and proto_num == num:
            return name[8:]
    return "Protocol not found"


# this func check the file if his extension is cap,pcap or pcapng
def file_integrity_check(file):
    split_tup = os.path.splitext(file)
    file_extension = split_tup[1]
    # print(split_tup)
    if file_extension == ".pcap":
        return True
    # TODO remember the cap,pcapng
    return False


# def read_from_line_file(line):
#     src_ip = str(line[IP].src)
#     list_IP_src.append(src_ip)
#     dst_ip = line[IP].dst
#     list_IP_dst.append(dst_ip)
#     src_mac = line[Ether].src
#     list_mac_src.append(src_mac)
#     dst_mac = line[Ether].dst
#     list_mac_dst.append(dst_mac)
#     list_protocol.append(proto_name_by_num(int(line[IP].proto)))


# def read_from_file_line_to_line(file):
#     packets = rdpcap(file)
#     for line in packets:
#         read_from_line_file(line)
#     return True


def file(file):
    if file_integrity_check(file) is False:
        return False
    return True


def get_mac_address(packet):
    src_mac = packet["Ether"].src
    dst_mac = packet["Ether"].dst
    return src_mac, dst_mac


def get_vendor(mac_address):
    return MacLookup().lookup(mac_address)


def get_device(mac_address):
    vendor = "no vendor."
    try:
        vendor = get_vendor(mac_address)
    except Exception:
        print("the device has no vendor")
    network_id = network.current_network.network_id
    device = Device(vendor=vendor, mac_address=mac_address, network_id=network_id)
    return device


def get_protocol(packet):
    protocol = proto_name_by_num(int(packet[IP].proto))
    return protocol


async def get_devices_to_add(pcap_file):
    devices = {}
    packets = rdpcap(fr'C:\Users\Owner\BOOTCAMP PYTHON\פרוייקט רשתות בשיתוף עם nvidia\קבצי cap לבדיקות\{pcap_file}')
    print("i reade the file into packets")
    for packet in packets:
        if packet.haslayer("Ether"):
            src_mac, dst_mac = get_mac_address(packet)
            protocol = get_protocol(packet)
            connection = Connection(src_mac_address=src_mac, dst_mac_address=dst_mac, protocol=protocol)
            if not devices.get(src_mac):
                src_device = get_device(src_mac)
                devices[src_mac] = {"device": src_device,
                                    "connections": []}

            if connection not in devices[src_mac]["connections"]:
                devices[src_mac]["connections"].append(connection)
            if not devices.get(dst_mac):
                dst_device = get_device(dst_mac)
                devices[dst_mac] = {"device": dst_device,
                                    "connections": []}

    return dict(devices)
