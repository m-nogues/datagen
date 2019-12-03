from scapy.all import *
from neo4j import GraphDatabase
import argparse
import json
import populate


def pcap_to_json(pcap):
    network = {}
    src_dst = []
    for packet in pcap:
        if IP in packet:
            src_dst += [(packet[IP].src, packet[IP].dst, packet[IP])]

    return network


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to generate a json representation of a ' +
        + 'network in a PCAP file')
    parser.add_argument('-u', '--user', nargs='?', default='neo4j',
                        help='The user to connect as')
    parser.add_argument('-p', '--password', nargs='?', default='neo4j',
                        help='The password to connect to neo4j')
    parser.add_argument('-a', '--address', nargs='?',
                        default='bolt://localhost:7687',
                        help='The url to connect to the server')
    parser.add_argument('pcap', nargs='+',
                        help='PCAP file containing the network to graph')
    args = parser.parse_args()

    # Initialisation
    driver = GraphDatabase.driver(
        args.address, auth=(args.user, args.password))

    for pcap in args.pcap:
        populate.network_import(driver, pcap_to_json(rdpcap(pcap)))
