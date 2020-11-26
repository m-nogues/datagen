import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to analyse a network in a PCAP file')
    parser.add_argument('pcap', nargs='*', help='PCAP file containing the network to graph', default=[])
    args = parser.parse_args()

    if len(sys.argv) >= 2:
        from model.pcap import main
        main(args.pcap)
    else:
        from view.view import main
        main()
