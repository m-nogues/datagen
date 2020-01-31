import random

import pandas as pd

from modules.generators import action_generator, crontab_generator
from modules.model import hacker


def rand_mac():
    """Generates a random mac address for a virtual machine
    
    Returns:
        str -- The generated mac address
    """
    return "08:00:27:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def rand_ip(prefixe):
    """Generates a random IP address with the given prefixe
    
    Arguments:
        prefixe {str} -- The prefixe for the generated IP address
    
    Returns:
        str -- The generated IP address
    """
    return prefixe + str(random.randint(3, 254))


def find_ip_and_mac(vms, prefixe):
    """Finds a random IP and mac address that is not used by the vms
    
    Arguments:
        vms {list} -- The list of vms to consider
        prefixe {str} -- The prefixe to use for the IP address
    
    Returns:
        str,str -- The IP and mac address generated
    """
    ips, macs = set(), set()
    for v in vms:
        ips.add(v.ip)
        macs.add(v.mac)

    ip = rand_ip(prefixe)
    while ip in ips:
        ip = rand_ip(prefixe)

    mac = rand_mac()
    while mac in macs:
        mac = rand_mac()

    return ip, mac


def prepare_hacker(conf, vms):
    """Generates the hacker with its actions, atacks, IP and mac address
    
    Arguments:
        conf {dict} -- The dictionnary containing the configuration
        vms {list} -- The list of vms to attack
    
    Returns:
        hacker -- The generated hacker
    """
    ip, mac = find_ip_and_mac(vms, conf['network']['prefixe'])
    h = hacker.hacker(ip, mac)

    for a in conf['hacker']['attacks']:
        h.add_attack(a)

    actions = action_generator.hacker(h, conf, vms)
    for a in actions:
        h.add_action(a)

    return h


def write_data(h):
    """Writes the hacker to a CSV file on disk
    
    Arguments:
        h {hacker} -- The hacker to write to disk
    """
    csv = {}
    for key, value in h.to_csv().items():
        if key in csv:
            csv[key] += [value]
        else:
            csv[key] = [value]

    df = pd.DataFrame(data=csv)

    keys = list(csv.keys())
    with open('vms/hacker.csv', 'w') as f:
        df.to_csv(path_or_buf=f, sep=',', index=False,
                  columns=keys)

    crontab_generator.hacker(h)


def generate(vms, conf, test):
    """Generates the hacker
    
    Arguments:
        vms {list} -- The list of vms
        conf {dict} -- The dictionnary containing the configuration
        test {boolean} -- Define if we need to write to disk or not
    
    Returns:
        hacker -- The generated hacker
    """
    h = prepare_hacker(conf, vms)

    if not test:
        write_data(h)

    return h
