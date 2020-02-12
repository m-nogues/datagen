import argparse
import json

from neo4j import GraphDatabase

from model import Machine, create_machine


def network_import(driver, network):
    # Creating the machines in Neo4J
    machines = {}
    for machine in network:
        machines[machine] = create_machine(driver, network[machine])

    # Creating the relations in Neo4J
    for machine in network:
        for rel in network[machine]["relations"]:
            if rel not in machines:
                continue
            for protocol in network[machine]["relations"][rel]:
                machines[machine].create_connection(
                    driver, machines[rel], protocol,
                    network[machine]["relations"][rel][protocol]
                )


if __name__ == "__main__":
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

    # Processing each JSON files passed as an argument
    for path in args.json:
        with open(path, 'r') as f:
            network = json.load(f)
        network_import(driver, network)

    driver.close()
