import os
from pathlib import Path
import socket
from scapy.all import *
from scapy.layers.inet import IP, Ether
from issuies.connection import Connection
from issuies.device import Device
from issuies.network import NetworkInDB

list_protocol = []
list_mac_dst = []
list_mac_src = []
list_IP_dst = []
list_IP_src = []


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


def read_from_line_file(line):
    src_ip = str(line[IP].src)
    list_IP_src.append(src_ip)
    dst_ip = line[IP].dst
    list_IP_dst.append(dst_ip)
    src_mac = line[Ether].src
    list_mac_src.append(src_mac)
    dst_mac = line[Ether].dst
    list_mac_dst.append(dst_mac)
    list_protocol.append(proto_name_by_num(int(line[IP].proto)))


def read_from_file_line_to_line(file):
    packets = rdpcap(file)
    for line in packets:
        read_from_line_file(line)
    return True


def file(file):
    if file_integrity_check(file) is False:
        # raise "The file is not correct"
        return False
    # print(read_from_file_line_to_line(file))
    # print(list_protocol)
    return True


# print(file("evidence04.pcap"))

# מיכל!
# מיכל!זה פונקציה מוכנה וטובה בשביל לקבל מהsourcוה dest את כתובת המאק שלהם הפונקציה צריכה לקבל את הפאקט כלומר שורה מהקובץ קאפ
# אולי כדאי לפצל את זה לשתי פונקציות :אחת שמחזירה את הכתובת מקא של הsrc והשניה את הכתובת מאק של ה dst



def get_device(packet, mac_address):
    # o_s = packet["Ether"].os
    o_s = "windows"
    network_id = NetworkInDB.network_id
    device = Device(operation_system=o_s, mac_address=mac_address, network_id=network_id)
    return device


def get_protocol(packet):
    # protocol=packet["Ether"].protocol
    protocol = "HTTP"
    return protocol



