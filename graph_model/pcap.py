import argparse
import json

from neo4j import GraphDatabase
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP

from populate import network_import
from tables import machine_behavior, flow_matrix, machine_role, machine_use


def pcap_to_json(pkt_file):
    network, ip_to_filter = {}, ['0.0.0.0', '224.0.0.22']
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

        # Create the machine if they don't already exist in our network
        if src not in network:
            network[src] = {"ip": src, "relations": {}}
        if dst not in network:
            network[dst] = {"ip": dst, "relations": {}}

        # Get ports depending on layer, also filter out layers that are not supported by the program
        if layer.haslayer(TCP):
            sport, dport = layer[TCP].sport, layer[TCP].dport
        elif layer.haslayer(UDP):
            sport, dport = layer[UDP].sport, layer[UDP].dport
        else:
            continue

        # Filter packets sent to an ephemeral port as they are sent as a response to a previous exchange
        if (49152 <= dport <= 65535) or (dst in network
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

    # Generate the JSON and the tables
    network = pcap_to_json(rdpcap(args.pcap))
    machine_behavior(network)
    machine_role(network)
    machine_use(network)
    flow_matrix(network)

    # Write to JSON
    with open('result.json', 'w') as f:
        json.dump(network, f, indent='\t')

    # If not a test, put the results in Neo4j
    if not args.test:
        # Sending to Neo4j
        driver = GraphDatabase.driver(
            args.address, auth=(args.user, args.password))
        network_import(driver, network)
        driver.close()
