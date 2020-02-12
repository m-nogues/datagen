import csv
from copy import deepcopy


def machine_behavior(network):
    table = deepcopy(network)
    for src in table:
        if not table[src]["relations"]:
            continue
        fields = ['\"Source\\Port\"'] + ['\"' + e + '\"' for e in table[src]["relations"]]
        ports = set()
        for dst in table[src]["relations"]:
            ports.update([*table[src]["relations"][dst]])
            total_pkt = 0
            for port in table[src]["relations"][dst]:
                total_pkt += table[src]["relations"][dst][port]
            for port in table[src]["relations"][dst]:
                table[src]["relations"][dst][port] = (table[src]["relations"][dst][port] / total_pkt) * 100
        with open('csv/machine_behavior-' + src + '.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for port in ports:
                row = {}
                for dst in table[src]["relations"]:
                    row['\"' + str(dst) + '\"'] = table[src]["relations"][dst][port] if port in table[src]["relations"][
                        dst] else 0
                if 0 >= sum(row.values()):
                    continue
                row['\"IP\\Port\"'] = port
                writer.writerow(row)


def flow_matrix(network):
    table = deepcopy(network)
    fields = ['\"Source\\Destination\"'] + ['\"' + e + '\"' for e in table]
    with open('csv/flow_matrix.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for src in table:
            if not table[src]["relations"]:
                continue
            row = {}
            for dst in table:
                row['\"' + str(dst) + '\"'] = sum(table[src]["relations"][dst].values()) if dst in table[src][
                    "relations"] else 0
            if 0 >= sum(row.values()):
                continue
            row['\"IP\\IP\"'] = src
            writer.writerow(row)


def machine_use(network):
    table = deepcopy(network)
    fields = ['\"IP\\Port\"']
    ports = set()
    for src in table:
        if not table[src]["relations"]:
            continue
        table[src]["ports"] = {}
        total_pkt = 0
        for dst in table[src]["relations"]:
            for port in table[src]["relations"][dst]:
                total_pkt += table[src]["relations"][dst][port]
                if port in table[src]["ports"]:
                    table[src]["ports"][port] += table[src]["relations"][dst][port]
                else:
                    table[src]["ports"][port] = table[src]["relations"][dst][port]
        for port in table[src]["ports"]:
            ports.add(port)
            table[src]["ports"][port] = (table[src]["ports"][port] / total_pkt) * 100

    fields += list('\"' + str(e) + '\"' for e in ports)
    with open('csv/machine_use.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for src in table:
            if not table[src]["relations"]:
                continue
            row = {}
            for port in ports:
                row["\"" + str(port) + "\""] = table[src]["ports"][port] if port in table[src]["ports"] else 0
            if 0 >= sum(row.values()):
                continue
            row['\"IP\\Port\"'] = src
            writer.writerow(row)


def machine_role(network):
    table = deepcopy(network)
    fields = ['\"IP\\Port\"']
    ports = set()
    for src in table:
        table[src]["ports"] = {}
    for src in table:
        if not table[src]["relations"]:
            continue
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
        total_pkt = 0
        for port in table[src]["ports"]:
            ports.add(port)
            total_pkt += table[src]["ports"][port]
        for port in table[src]["ports"]:
            table[src]["ports"][port] = (table[src]["ports"][port] / total_pkt) * 100

    fields += list('\"' + str(e) + '\"' for e in ports)
    with open('csv/machine_role.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for src in table:
            if not table[src]["relations"]:
                continue
            row = {}
            for port in ports:
                row["\"" + str(port) + "\""] = table[src]["ports"][port] if port in table[src]["ports"] else 0
            if 0 >= sum(row.values()):
                continue
            row['\"IP\\Port\"'] = src
            writer.writerow(row)
