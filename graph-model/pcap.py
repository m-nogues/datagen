import json

from scapy.all import *
from neo4j import GraphDatabase
import argparse
from populate import network_import
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6


def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x


def nb_pkt_to_percentage(network):
    for src in network:
        for dst in network[src]["relations"]:
            total_pkt = 0
            for port in network[src]["relations"][dst]:
                total_pkt += network[src]["relations"][dst][port]
            for port in network[src]["relations"][dst]:
                network[src]["relations"][dst][port] = (network[src]["relations"][dst][port] / total_pkt) * 100
    return network


def pcap_to_json(pkt_file):
    network = {}
    for p in pkt_file:
        if p.haslayer(IP):
            layer = p[IP]
            src, dst = layer.src, layer.dst
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
    parser.add_argument('pcap', nargs='+',
                        help='PCAP file containing the network to graph')
    args = parser.parse_args()

    # Test
    if args.test:
        i = 0
        for pcap in args.pcap:
            with open('result_' + str(i) + '.json', 'w') as f:
                json.dump(pcap_to_json(rdpcap(pcap)), f)
            i += 1
    else:
        # Initialisation
        driver = GraphDatabase.driver(
            args.address, auth=(args.user, args.password))

        for pcap in args.pcap:
            network_import(driver, pcap_to_json(rdpcap(pcap)))
