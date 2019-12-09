import json

from scapy.all import *
from neo4j import GraphDatabase
import argparse
from populate import network_import
from tables import machine_behavior, flow_matrix, machine_role
from scapy.layers.inet import IP, TCP, UDP
# from scapy.layers.inet6 import IPv6


def pcap_to_json(pkt_file):
    network = {}
    for p in pkt_file:
        if p.haslayer(IP):
            layer = p[IP]
            src, dst = layer.src, layer.dst
            if src == '0.0.0.0' or dst == '0.0.0.0':
                continue
            if src not in network:
                network[src] = {"ip": src, "relations": {}}
            if layer.haslayer(TCP):
                sport, dport = layer[TCP].sport, layer[TCP].dport
                if (1024 < dport < 5000) or (32768 < dport < 65535):
                    continue
                if dst in network[src]["relations"]:
                    if dport in network[src]["relations"][dst]:
                        network[src]["relations"][dst][dport] += 1
                    else:
                        network[src]["relations"][dst][dport] = 1
                else:
                    network[src]["relations"][dst] = {dport: 1}
            elif layer.haslayer(UDP):
                sport, dport = layer[UDP].sport, layer[UDP].dport
                if dport > 1024:
                    continue
                if dst in network[src]["relations"]:
                    if dport in network[src]["relations"][dst]:
                        network[src]["relations"][dst][dport] += 1
                    else:
                        network[src]["relations"][dst][dport] = 1
                else:
                    network[src]["relations"][dst] = {dport: 1}
        # if p.haslayer(IPv6):
        #     layer = p[IPv6]
        #     src, dst = layer.src, layer.dst
        #     if src not in network:
        #         network[src] = {"ip": src, "relations": {}}
        #     if layer.haslayer(TCP):
        #         sport, dport = layer[TCP].sport, layer[TCP].dport
        #         if dst in network and src in network[dst]["relations"] and sport in network[dst]["relations"][src]:
        #             continue
        #         if dst in network[src]["relations"]:
        #             if dport in network[src]["relations"][dst]:
        #                 network[src]["relations"][dst][dport] += 1
        #             else:
        #                 network[src]["relations"][dst][dport] = 1
        #         else:
        #             network[src]["relations"][dst] = {dport: 1}
        #     elif layer.haslayer(UDP):
        #         sport, dport = layer[UDP].sport, layer[UDP].dport
        #         if dst in network and src in network[dst]["relations"] and sport in network[dst]["relations"][src]:
        #             continue
        #         if dst in network[src]["relations"]:
        #             if dport in network[src]["relations"][dst]:
        #                 network[src]["relations"][dst][dport] += 1
        #             else:
        #                 network[src]["relations"][dst][dport] = 1
        #         else:
        #             network[src]["relations"][dst] = {dport: 1}
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

    # Test
    if args.test:
        network = pcap_to_json(rdpcap(args.pcap))

        machine_role(network)

        with open('result.json', 'w') as f:
            json.dump(network, f)
    else:
        # Initialisation
        driver = GraphDatabase.driver(
            args.address, auth=(args.user, args.password))

        network = pcap_to_json(rdpcap(args.pcap))

        network_import(driver, network)
