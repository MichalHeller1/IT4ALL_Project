# import os
# import pyshark
from scapy.all import *


# this func check the file if his extension is cap,pcap or pcapng
def file_integrity_check(file):
    split_tup = os.path.splitext(file)
    file_extension = split_tup[1]
    print(split_tup)
    if file_extension == ".pcap":
        return True
    # TODO remember the cap,pcapng
    return False

def read_from_cap_file_line_to_line(file):
    packets = rdpcap(file)
    lines_packets=[]
    for i in packets:
        lines_packets.append(i)
    return lines_packets
def file(file):
    if file_integrity_check(file) is False:
        # raise "The file is not correct"
        return False
    values_file_line_to_line = read_from_cap_file_line_to_line(file)
    if len(values_file_line_to_line) <= 0:
        return False
    # send to function that get the value from cap at obj to the DB
    return True


print(file("evidence04.pcap"))
