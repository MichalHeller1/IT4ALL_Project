import os
# import pyshark
from scapy.all import rdpcap, IP, Ether

list_IP_src = []
list_IP_dst = []
list_mac_src = []
list_mac_dst = []


# this func check the file if his extension is cap,pcap or pcapng
def file_integrity_check(file):
    split_tup = os.path.splitext(file)
    file_extension = split_tup[1]
    print(split_tup)
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


def read_from_file_line_to_line(file):
    packets = rdpcap(file)
    for line in packets:
        read_from_line_file(line)
    return True


def file(file):
    if file_integrity_check(file) is False:
        # raise "The file is not correct"
        return False
    print(read_from_file_line_to_line(file))
    # print(list_mac_dst)
    return True


print(file("evidence04.pcap"))
