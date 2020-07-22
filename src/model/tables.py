import os
from copy import deepcopy

import pandas as pd


def write_rows(name, fields, rows):
    """
    Writes the rows in a CSV file named with name. The first line is the fields.
    :param name: the name of the file
    :param fields: the fields of the CSV
    :param rows: the rows of the CSV
    """

    # Creates missing directories in the name of the file
    dirs = os.path.dirname(name)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    # Adds the fields names
    df = pd.DataFrame(rows).set_index(fields[0])

    # Sorts the table in descending order for columns and rows
    df = df.assign(tmp=df.sum(axis=1)).sort_values('tmp', ascending=False).drop('tmp', 1).T.assign(
        tmp=df.T.sum(axis=1)).sort_values('tmp', ascending=False).drop('tmp', 1).T

    # Writes the sorted table to the CSV file
    df.to_csv(name)


def machine_behavior(network, name):
    """
    Creates the tables describing the behavior of the machines in the network
    :param name: the name of the pcap file tested
    :param network: the description of the network
    """
    table = deepcopy(network)
    for src in table:
        fields = ['Source\\Destination port'] + [str(e) for e in table[src]["relations"]]
        ports = set()
        rows = list()
        for dst in table[src]["relations"]:
            ports.update([*table[src]["relations"][dst]])
        for port in ports:
            row = {'Source\\Destination port': str(port)}
            for dst in table[src]["relations"]:
                row[str(dst)] = table[src]["relations"][dst][port] if port in table[src]["relations"][
                    dst] else 0
            if 0 >= sum([e if type(e) is int else 0 for e in row.values()]):
                continue
            rows += [row]
        write_rows(str(name + '/csv/machine_behavior-' + src + '.csv'), fields, rows)


def flow_matrix(network, name):
    """
    Creates the flow matrix corresponding to the network
    :param name: the name of the pcap file tested
    :param network: the description of the network
    """
    table = deepcopy(network)
    fields = ['Source\\Destination'] + [str(e) for e in table]
    rows = list()
    for src in table:
        row = {'Source\\Destination': str(src)}
        for dst in table:
            row[str(dst)] = sum(table[src]["relations"][dst].values()) if dst in table[src][
                "relations"] else 0
        if 0 >= sum([e if type(e) is int else 0 for e in row.values()]):
            continue
        rows += [row]
    write_rows(name + '/csv/flow_matrix.csv', fields, rows)


def machine_use(network, name):
    """
    Creates the table describing the use of the machines in the network
    :param name: the name of the pcap file tested
    :param network: the description of the network
    """
    table = deepcopy(network)
    fields = ['Source\\Destination port']
    ports = set()
    for src in table:
        table[src]["ports"] = {}
        for dst in table[src]["relations"]:
            for port in table[src]["relations"][dst]:
                if port in table[src]["ports"]:
                    table[src]["ports"][port] += table[src]["relations"][dst][port]
                else:
                    table[src]["ports"][port] = table[src]["relations"][dst][port]
        ports.update(table[src]["ports"])

    fields += list(str(e) for e in ports)
    rows = list()
    for src in table:
        row = {'Source\\Destination port': str(src)}
        for port in ports:
            row[str(port)] = table[src]["ports"][port] if port in table[src]["ports"] else 0
        if 0 >= sum([e if type(e) is int else 0 for e in row.values()]):
            continue
        rows += [row]
    write_rows(name + '/csv/machine_use.csv', fields, rows)


def machine_role(network, name):
    """
    Creates the table describing the role of the machines in the network
    :param name: the name of the pcap file tested
    :param network: the description of the network
    """
    table = deepcopy(network)
    fields = ['Source\\Port']
    ports = set()
    for src in table:
        table[src]["ports"] = {}
    for src in table:
        for dst in table[src]["relations"]:
            if dst not in table:
                continue
            for port in table[src]["relations"][dst]:
                if port in table[dst]["ports"]:
                    table[dst]["ports"][port] += table[src]["relations"][dst][port]
                else:
                    table[dst]["ports"][port] = table[src]["relations"][dst][port]
    for src in table:
        if not table[src]["relations"]:
            continue
        ports.update(table[src]["ports"])

    fields += list(str(e) for e in ports)
    rows = list()
    for src in table:
        row = {'Source\\Port': str(src)}
        for port in ports:
            row[str(port)] = table[src]["ports"][port] if port in table[src]["ports"] else 0
        if 0 >= sum([e if type(e) is int else 0 for e in row.values()]):
            continue
        rows += [row]
    write_rows(name + '/csv/machine_role.csv', fields, rows)