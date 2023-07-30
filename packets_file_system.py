# import os
# import pyshark
from pathlib import Path

from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6

from issuies import network
from issuies.connection import Connection
from issuies.device import Device
from issuies.network import NetworkInDB


# this func check the file if his extension is cap,pcap or pcapng
def file_integrity_check(file):
    split_tup = os.path.splitext(file)
    file_extension = split_tup[1]
    # print(split_tup)
    if file_extension == ".pcap":
        return True
    # TODO remember the cap,pcapng
    return False


#
# def read_from_cap_file_line_to_line(file):
#     packets = rdpcap(file)
#     lines_packets=[]
#     for i in packets:
#         lines_packets.append(i)
#     return lines_packets
def file(file):
    if file_integrity_check(file) is False:
        # raise "The file is not correct"
        return False
    # values_file_line_to_line = read_from_cap_file_line_to_line(file)
    # if len(values_file_line_to_line) <= 0:
    #     return False
    # send to function that get the value from cap at obj to the DB
    return True


async def get_mac_addresses_from_pcap(pcap_file):
    # TODO:change this function to get_device_from_pcap_file and this func will use this func and it will create a device from every mac address and to return it in list of devices
    mac_addresses = set()  # Use a set to avoid duplicates
    # TODO: let the user to insert file from every location on his computer
    # now you can insert a file just from the location that you can change here.
    packets = rdpcap(fr'C:\Users\Owner\BOOTCAMP PYTHON\פרוייקט רשתות בשיתוף עם nvidia\קבצי cap לבדיקות\{pcap_file}')
    for packet in packets:
        if packet.haslayer("Ether"):
            src_mac = packet["Ether"].src
            dst_mac = packet["Ether"].dst
            mac_addresses.add(src_mac)
            mac_addresses.add(dst_mac)
    return list(mac_addresses)


# מיכל!
# מיכל!זה פונקציה מוכנה וטובה בשביל לקבל מהsourcוה dest את כתובת המאק שלהם הפונקציה צריכה לקבל את הפאקט כלומר שורה מהקובץ קאפ
# אולי כדאי לפצל את זה לשתי פונקציות :אחת שמחזירה את הכתובת מקא של הsrc והשניה את הכתובת מאק של ה dst
def get_mac_address(packet):
    src_mac = packet["Ether"].src
    dst_mac = packet["Ether"].dst
    return src_mac, dst_mac


def get_device(packet, mac_address):
    # o_s = packet["Ether"].os
    o_s = "linux"
    network_id = network.current_network.network_id
    device = Device(operation_system=o_s, mac_address=mac_address, network_id=network_id)
    return device


def get_protocol(packet):
    # protocol=packet["Ether"].protocol
    protocol = "HTTP"
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
                src_device = get_device(packet, src_mac)
                devices[src_mac] = {"device": src_device,
                                    "connections": []}

            if connection not in devices[src_mac]["connections"]:
                devices[src_mac]["connections"].append(connection)
            if not devices.get(dst_mac):
                dst_device = get_device(packet, dst_mac)
                devices[dst_mac] = {"device": dst_device,
                                    "connections": []}

    return dict(devices)
