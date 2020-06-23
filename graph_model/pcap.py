import argparse
import json

from neo4j import GraphDatabase
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP

from populate import network_import
from tables import machine_behavior, flow_matrix, machine_role, machine_use

# The list of IP address to filter from the PCAPs
ip_to_filter = ['0.0.0.0', '224.0.0.22']


def pcap_to_json(pkt_file):
    """
    Analyses the PCAP file and creates the JSON description of the network it represents
    :param pkt_file: the PCAP file
    :return: the network as a python dictionary / JSON
    """
    network = {}
    for p in pkt_file:
        # Filter packets not having an IP layer
        if p.haslayer(IP):
            layer = p[IP]
        # elif p.haslayer(IPv6):
        #     layer = p[IPv6]
        else:
            continue

        src, dst = layer.src, layer.dst

        # Filtering sources and destination to not treat broadcast IP as a machine in the network
        if src in ip_to_filter or ('255' in dst.split('.') or dst in ip_to_filter):
            continue

        # Creates the machine if they don't already exist in our network
        if src not in network:
            network[src] = {"ip": src, "relations": {}}
        if dst not in network:
            network[dst] = {"ip": dst, "relations": {}}

        # Gets ports depending on layer, also filter out layers that are not supported by the program
        if layer.haslayer(TCP):
            sport, dport = layer[TCP].sport, layer[TCP].dport
        elif layer.haslayer(UDP):
            sport, dport = layer[UDP].sport, layer[UDP].dport
        else:
            continue

        # Filters packets sent to an ephemeral port as they are sent as a response to a previous exchange
        if (32768 <= dport <= 65535) or (dst in network
                                         and src in network[dst]["relations"]
                                         and sport in network[dst]["relations"][src]):
            continue

        # Add the packets to our recording of the network
        if dst in network[src]["relations"]:
            if dport in network[src]["relations"][dst]:
                network[src]["relations"][dst][dport] += 1
            else:
                network[src]["relations"][dst][dport] = 1
        else:
            network[src]["relations"][dst] = {dport: 1}
    network = {k: v for k, v in network.items() if network[k]["relations"]}
    return network


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to generate a json representation of a '
                    + 'network in a PCAP file')
    parser.add_argument('-u', '--user', nargs='?', default='neo4j',
                        help='The user to connect as')
    parser.add_argument('-p', '--password', nargs='?', default='neo4j',
                        help='The password to connect to neo4j')
    parser.add_argument('-a', '--address', nargs='?',
                        default='bolt://localhost:7687',
                        help='The url to connect to the server')
    parser.add_argument('-t', '--test', action='store_true',
                        help='allows to run the script to just generate the json files')
    parser.add_argument('pcap', help='PCAP file containing the network to graph')
    args = parser.parse_args()

    # Generates the JSON
    network = pcap_to_json(rdpcap(args.pcap))

    # Writes to JSON
    name = '.'.join(os.path.basename(args.pcap).split(".")[0:-1])
    if not os.path.exists(name):
        os.makedirs(name)
    with open(name + '/result.json', 'w') as f:
        json.dump(network, f, indent='\t')

    # Generates the tables
    machine_behavior(network, name)
    machine_role(network, name)
    machine_use(network, name)
    flow_matrix(network, name)

    # If not a test, put the results in Neo4j
    if not args.test:
        # Sending to Neo4j
        driver = GraphDatabase.driver(
            args.address, auth=(args.user, args.password))
        network_import(driver, network)
        driver.close()
