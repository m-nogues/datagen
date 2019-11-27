#!/usr/bin/python
import argparse
import json

from neo4j import GraphDatabase

import model


def network_import(driver, json):
    # Processing
    machines = {}
    for machine in json:
        machines[machine] = model.Machine.create_machine(
            driver, json[machine]['name'], json[machine]['ip'])

    for machine in json:
        for rel in json[machine]['relations']:
            for protocol in json[machine]['relations'][rel]:
                machines[machine].create_connection(
                    driver, machines[rel], protocol,
                    json[machine]['relations'][rel][protocol]
                )


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(
        description='Python script to graph a network model')
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
        network = {}
        with open(path, 'r') as f:
            network = json.load(f)
        network_import(driver, network)

    driver.close()
