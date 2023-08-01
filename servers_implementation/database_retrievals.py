from matplotlib import image as mpimg
from issuies.connection import Connection, DevicesConnection
from issuies.device import Device
import networkx as nx
import matplotlib.pyplot as plt
import os

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
        G.add_edge(mac_address_1, mac_address_2, label=connection.protocol)  # Label for edge between devices

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=900)  # You can try different layout algorithms here

    # Load the image for the "main router" node
    main_router_image = mpimg.imread(router_image_path)
    G.nodes["main router"]['image'] = main_router_image

    # Draw the nodes using pictures
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
    plt.show()


# Example usage:
# visualize_network_graph(connections_lst)


# Call the function with your connections data
device1 = Device(vendor="some vendor 1", mac_address="1", network_id=1)
device2 = Device(vendor="some vendor 2", mac_address="2", network_id=1)
device3 = Device(vendor="some vendor 3", mac_address="3", network_id=1)
device4 = Device(vendor="some vendor 4", mac_address="4", network_id=1)
device5 = Device(vendor="some vendor 5", mac_address="5", network_id=1)

connection = DevicesConnection(src_device=device1, dst_device=device2, protocol="HTTP")
connection2 = DevicesConnection(src_device=device1, dst_device=device3, protocol="HTTP")
connection3 = DevicesConnection(src_device=device2, dst_device=device1, protocol="HTTP")
connection4 = DevicesConnection(src_device=device3, dst_device=device2, protocol="HTTP")
connection5 = DevicesConnection(src_device=device1, dst_device=device5, protocol="HTTP")
connection6 = DevicesConnection(src_device=device1, dst_device=device4, protocol="HTTP")
connection7 = DevicesConnection(src_device=device5, dst_device=device1, protocol="HTTP")
connections = [connection, connection2, connection3, connection4, connection5, connection6, connection7]
visualize_network_graph(connections)
