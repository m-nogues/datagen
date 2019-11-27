import scapy
import argparse
import json

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
    args = parser.parse_args()

    
