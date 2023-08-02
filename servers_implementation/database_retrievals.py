from DB_Implementatins import db_retrievals_implementation
from global_modules import visualize_graph
from issues.connection import DevicesConnection
from issues.device import Device


async def visualize_network_graph(connections_lst):
    pic_graph = await visualize_graph.get_the_complete_graph(connections_lst)
    return pic_graph


async def get_connections_in_specific_network(network_id):
    connections_lst = await db_retrievals_implementation.get_network_connections(network_id)
    complete_connections = []

    for connection in connections_lst:
        mac_address1 = connection[1]
        vendor1 = connection[2]
        network_id1 = 1

        mac_address2 = connection[3]
        vendor2 = connection[4]
        network_id2 = 1

        device1 = Device(vendor=vendor1, mac_address=mac_address1, network_id=network_id1)
        device2 = Device(vendor=vendor2, mac_address=mac_address2, network_id=network_id2)

        full_connection = DevicesConnection(src_device=device1, dst_device=device2, protocol=connection[0])
        complete_connections.append(full_connection)

    return complete_connections


async def get_lst_of_devices(network_id):
    devices = await db_retrievals_implementation.get_devices_by_network_id(network_id)
    if devices:
        return list(devices)
    else:
        return None


async def check_client_id_in_db(client_id):
    try:
        client = await db_retrievals_implementation.get_client(client_id)
        return client
    except Exception:
        return None
