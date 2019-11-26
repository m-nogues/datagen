#!/usr/bin/python
import argparse
import json

from neo4j import GraphDatabase

import model


def network_import(driver, path):
    network = {}
    with open(path, 'r') as f:
        network = json.load(f)

    # Processing
    machines = {}
    for machine in network:
        machines[machine] = model.Machine.create_machine(
            driver, network[machine]['name'], network[machine]['ip'])

    for machine in network:
        for rel in network[machine]['relations']:
            for protocol in network[machine]['relations'][rel]:
                machines[machine].create_connection(
                    driver, machines[rel], protocol,
                    network[machine]['relations'][rel][protocol]
                )


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(
        description='Python framework for an easy creation of a network model')
    parser.add_argument('-u', '--user', nargs='?', default='neo4j',
                        help='The user to connect as')
    parser.add_argument('-p', '--password', nargs='?', default='neo4j',
                        help='The password to connect to neo4j')
    parser.add_argument('-a', '--address', nargs='?',
                        default='bolt://localhost:7687',
                        help='The url to connect to the server')
    parser.add_argument('json', nargs='+',
                        help='JSON file containing the network to graph')
    args = parser.parse_args()

    # Initialisation
    driver = GraphDatabase.driver(
        args.address, auth=(args.user, args.password))

    for path in args.json:
        network_import(driver, path)

    driver.close()
