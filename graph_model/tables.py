import csv
from copy import deepcopy

import pandas as pd


def write_rows(name, fields, rows):
    """
    Writes the rows in a CSV file named with name. The first line is the fields.
    :param name: the name of the file
    :param fields: the fields of the CSV
    :param rows: the rows of the CSV
    """
    df = pd.DataFrame(rows).set_index(fields[0])
    df = df = df.assign(tmp=df.sum(axis=1)).sort_values('tmp', ascending=False).drop('tmp', 1).T.assign(
        tmp=df.T.sum(axis=1)).sort_values('tmp', ascending=False).drop('tmp', 1).T
    df.to_csv(name)


def machine_behavior(network):
    """
    Creates the tables describing the behavior of the machines in the network
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
        write_rows(str('csv/machine_behavior-' + src + '.csv'), fields, rows)


def flow_matrix(network):
    """
    Creates the flow matrix corresponding to the network
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
    write_rows('csv/flow_matrix.csv', fields, rows)


def machine_use(network):
    """
    Creates the table describing the use of the machines in the network
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
    write_rows('csv/machine_use.csv', fields, rows)


def machine_role(network):
    """
    Creates the table describing the role of the machines in the network
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
    write_rows('csv/machine_role.csv', fields, rows)
