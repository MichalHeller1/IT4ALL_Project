import networkx as nx
import matplotlib.pyplot as plt

from issuies.connection import Connection, DevicesConnection
from issuies.device import Device


def visualize_network_graph(connections_lst):
    # Create an empty graph
    G = nx.Graph()
    # Add nodes (devices) and their vendors to the graph
    for connection in connections_lst:
        device1, device2 = connection
        mac_address_1, protocol =device1.mac_address, device1.vendor
        mac_address_2, protocol =device2.mac_address, device2.vendor
        G.add_node(mac_address_1, protocol=protocol)
        G.add_node(mac_address_2, protocol=protocol)

        # Add edges (connections) between devices
        G.add_edge(mac_address_1, mac_address_2)

    # Generate the visual representation of the network graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=5)  # You can try different layout algorithms here
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=8, font_weight='bold')
    node_labels = nx.get_node_attributes(G, 'vendor')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    # Save or show the plot
    plt.savefig('network_graph.png')
    plt.show()


# Call the function with your connections data
device1 = Device(vendor="some vendor 1", mac_address="2:2:55:4:55")
device2 = Device(vendor="some vendor 2", mac_address="2:2:55:6:5:6")
connections = [DevicesConnection(device1, device2),
               DevicesConnection(device1, device2),
               DevicesConnection(device1, device2),
               DevicesConnection(device1, device2)]
visualize_network_graph(connections)
