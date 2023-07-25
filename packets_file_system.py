import os
import pyshark


# this func check the file if his extension is cap,pcap or pcapng
def file_integrity_check(file):
    split_tup = os.path.splitext(file)
    file_extension = split_tup[1]
    print(split_tup)
    if file_extension == ".pcap":
        return True
    # TODO remember the cap,pcapng
    return False

#TODO dont touchhhhhhh
def read_from_cap_file(file):
    # try to read from file and return it
    # but if cant return ""
    # here I have=> raise "It was not possible to read from the file"
    # cap = pyshark.FileCapture(file)
    # print(type(cap))
    # print(len(str(cap)))
    # # cap[0].sv.get_field_by_showname("evidence04.pcap")
    # print((cap[0]["IP"]))
    # l = cap[0].layers
    # print(str(l[1]))
    # a = []
    # pdml = .objectify.fromstring(xml_data)
    # packets = []
    #
    # for xml_pkt in pdml.getchildren():
    #     packets += [packet_from_xml_packet(xml_pkt)]
    #
    # # print(list(cap[0]))
    # # for i in cap:
    # #     try:
    # #         print(i['IP'].srcport)
    # #         a.append(i['TCP'].srcport)
    # #     except:
    # #         print('None')
    # #         a.append(0)
    # # print(a[0])
    return "njnk"


def file(file):
    if file_integrity_check(file) is False:
        # raise "The file is not correct"
        return False
    values_file = read_from_cap_file(file)
    if len(values_file) <= 0:
        return False
    # send to function that get the value from cap at obj to the DB
    return True


print(file("evidence04.pcap"))
