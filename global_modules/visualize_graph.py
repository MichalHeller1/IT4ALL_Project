from matplotlib import image as mpimg
import networkx as nx
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
node_image_path = os.path.join(current_dir, "nodes_icons", "computer-screen_2493283.png")
router_image_path = os.path.join(current_dir, "nodes_icons", "internet_9536354.png")
image_size = (0.1, 0.1)


def create_graph(list_to_create_the_graph):
    G = nx.Graph()

    for connection in list_to_create_the_graph:
        device1, device2 = connection.src_device, connection.dst_device

        mac_address_1, vendor_1 = device1.mac_address, device1.vendor
        mac_address_2, vendor_2 = device2.mac_address, device2.vendor
        G.add_edge(mac_address_1, "main router")
        G.add_edge(mac_address_2, "main router")
        G.add_edge(mac_address_1, mac_address_2, label=connection.protocol)

    return G


def draw_nodes(G, pos):
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


def draw_edges(G, pos):
    nx.draw_networkx_edges(G, pos, edge_color='gray')


def draw_labels(G, pos):
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)


def save_graph_image(G, pos):
    plt.axis('off')
    plt.savefig('network_graph.png')


async def get_the_complete_graph(list_to_create_the_graph):
    G = create_graph(list_to_create_the_graph)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=900)

    draw_nodes(G, pos)
    draw_edges(G, pos)
    draw_labels(G, pos)
    save_graph_image(G, pos)

    return 'network_graph.png'
