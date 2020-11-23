import argparse
import json

from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP

from tables import flow_matrix, indicators, machine_behavior, machine_role, machine_use

# The list of IP address to filter from the PCAPs
ip_to_filter = ['0.0.0.0', '224.0.0.22', '224.0.0.252']


def pcap_to_json(pkt_file):
    """
    Analyses the PCAP file and creates the JSON description of the network it represents
    :param pkt_file: the PCAP file
    :return: the network as a python dictionary / JSON
    """
    pcap = {'network': {}}
    for p in pkt_file:
        # Define the end of the PCAP to the time of the packet until the last one
        pcap['end'] = float(p.time)
        # Define the start of the PCAP to the time of the packet only for the first one
        if 'start' not in pcap:
            pcap['start'] = float(p.time)
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

        # Gets ports depending on layer, also filter out layers that are not supported by the program
        if layer.haslayer(TCP):
            sport, dport = layer[TCP].sport, layer[TCP].dport
        elif layer.haslayer(UDP):
            sport, dport = layer[UDP].sport, layer[UDP].dport
        else:
            continue

        # Creates the machine if they don't already exist in our network
        if src not in pcap['network']:
            pcap['network'][src] = {"ip": src, "relations": {}, 'start': float(p.time), 'end': float(p.time)}
        if dst not in pcap['network']:
            pcap['network'][dst] = {"ip": dst, "relations": {}, 'start': float(p.time), 'end': float(p.time)}

        # Sets the end of life of both source and destination machine to the time of arrival of the current packet
        pcap['network'][src]['end'] = pcap['network'][dst]['end'] = float(p.time)

        # Flag packets sent to an ephemeral port as response to a previous exchange
        if (32768 <= dport <= 65535) or (dst in pcap['network']
                                         and src in pcap['network'][dst]["relations"]
                                         and sport in pcap['network'][dst]["relations"][src]):
            if src not in pcap['network'][dst]["relations"]:
                pcap['network'][dst]["relations"][src] = {}
            if "response" in pcap['network'][dst]["relations"][src]:
                pcap['network'][dst]["relations"][src]["response"] += 1
            else:
                pcap['network'][dst]["relations"][src]["response"] = 1
            continue

        # Add the packets to our recording of the network
        if dst in pcap['network'][src]["relations"]:
            if dport in pcap['network'][src]["relations"][dst]:
                pcap['network'][src]["relations"][dst][dport] += 1
            else:
                pcap['network'][src]["relations"][dst][dport] = 1
        else:
            pcap['network'][src]["relations"][dst] = {dport: 1}

    # Filter out the machines with no relations in our network
    pcap['network'] = {k: v for k, v in pcap['network'].items() if pcap['network'][k]["relations"]}

    return pcap


def main(pcap_file):
    # Creates a directory named the same as the PCAP file
    name = '.'.join(os.path.basename(pcap_file).split(".")[0:-1])
    if not os.path.exists(name):
        os.makedirs(name)

    # Generates the JSON
    if not os.path.exists(name + '/result.json'):
        pcap = pcap_to_json(rdpcap(pcap_file))

        # Writes to JSON
        with open(name + '/result.json', 'w') as f:
            json.dump(pcap, f, indent='\t')
    else:
        with open(name + '/result.json', 'r') as f:
            pcap = json.load(f)

    # Generates the tables
    machine_behavior(pcap['network'], name)
    machine_role(pcap['network'], name)
    machine_use(pcap['network'], name)
    flow_matrix(pcap['network'], name)
    indicators(pcap, name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to generate a json representation of a '
                    + 'network in a PCAP file')
    parser.add_argument('pcap', help='PCAP file containing the network to graph')
    args = parser.parse_args()

    main(args.pcap)
