from matplotlib import image as mpimg
import networkx as nx
import matplotlib.pyplot as plt
import os

from DB_Implementatins import db_retrievals_implementation
from issues.connection import DevicesConnection
from issues.device import Device

current_dir = os.path.dirname(os.path.abspath(__file__))
node_image_path = os.path.join(current_dir, "nodes_icons", "computer-screen_2493283.png")
router_image_path = os.path.join(current_dir, "nodes_icons", "internet_9536354.png")
image_size = (0.1, 0.1)


def visualize_network_graph(connections_lst):
    G = nx.Graph()

    for connection in connections_lst:
        device1, device2 = connection.src_device, connection.dst_device

        mac_address_1, vendor_1 = device1.mac_address, device1.vendor
        mac_address_2, vendor_2 = device2.mac_address, device2.vendor
        G.add_edge(mac_address_1, "main router")
        G.add_edge(mac_address_2, "main router")
        G.add_edge(mac_address_1, mac_address_2, label=connection.protocol)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=900)  # You can try different layout algorithms here

    main_router_image = mpimg.imread(router_image_path)
    G.nodes["main router"]['image'] = main_router_image

    nx.draw_networkx_nodes(G, pos, nodelist=["main router"], node_size=0, node_color='skyblue', alpha=0.7)
    for node in G.nodes():
        if node != "main router" and node in pos:
            plt.imshow(mpimg.imread(node_image_path),
                       extent=[pos[node][0] - image_size[0] / 2, pos[node][0] + image_size[0] / 2,
                               pos[node][1] - image_size[1] / 2, pos[node][1] + image_size[1] / 2],
                       aspect='auto', zorder=0)
        elif node == "main router" and node in pos:
            plt.imshow(G.nodes[node]['image'],
                       extent=[pos[node][0] - image_size[0] / 2, pos[node][0] + image_size[0] / 2,
                               pos[node][1] - image_size[1] / 2, pos[node][1] + image_size[1] / 2],
                       aspect='auto', zorder=0)

    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.axis('off')
    plt.savefig('network_graph.png')
    # plt.show()
    return 'network_graph.png'


async def get_connections_in_specific_network(network_id):
    decoded_connections = await db_retrievals_implementation.get_network_connections(network_id)
    full_connections = []

    for connection in decoded_connections:
        mac_address1 = connection[1]
        vendor1 = connection[2]
        network_id1 = 1

        mac_address2 = connection[3]
        vendor2 = connection[4]
        network_id2 = 1

        device1 = Device(vendor=vendor1, mac_address=mac_address1, network_id=network_id1)
        device2 = Device(vendor=vendor2, mac_address=mac_address2, network_id=network_id2)

        full_connection = DevicesConnection(src_device=device1, dst_device=device2, protocol=connection[0])
        full_connections.append(full_connection)

    return full_connections
