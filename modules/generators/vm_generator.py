import random

import pandas as pd

from modules.generators import action_generator, crontab_generator
from modules.model import behavior, vm


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


def rand_services(services):
    """Choose a set of random services in the given set of services
    
    Arguments:
        services {set} -- The set of services
    
    Returns:
        set -- The set of chosen services
    """
    ret = set()
    number_of_services = random.randint(1, len(services))
    while len(ret) < number_of_services:
        ret.add(random.sample(services, 1)[0])

    return ret


def rand_ip(prefixe):
    """Generates a random IP address with the given prefixe
    
    Arguments:
        prefixe {str} -- The prefixe for the generated IP address
    
    Returns:
        str -- The generated IP address
    """
    return prefixe + str(random.randint(3, 254))


def gen_rand_ip_and_mac(vms, number_of_vms, prefixe):
    """Generates a random IP and mac address considering the previously generated couples to keep them in couple if we generate the same IP or mac a second time
    
    Arguments:
        vms {list} -- The list of previously generated vms
        number_of_vms {int} -- The number of vms
        prefixe {str} -- The prefixe for the IP address generation
    
    Returns:
        str,str -- The generated IP and mac address
    """
    ip = rand_ip(prefixe)
    mac = rand_mac()
    exists = False
    for v in vms:
        if v.ip == ip:
            mac, exists = v.mac, True
        elif v.mac == mac:
            ip, exists = v.ip, True
        if int(len(vms) / number_of_vms) == int(vms.index(v) / number_of_vms) and exists:
            ip, mac = gen_rand_ip_and_mac(vms, number_of_vms, prefixe)
            break

    return ip, mac


def gen_vm(vms, number_of_vms, prefixe, services):
    """Generates a vm
    
    Arguments:
        vms {list} -- The list of the vms
        number_of_vms {int} -- The number of physical vms
        prefixe {str} -- The prefixe for the IP address generation
        services {set} -- The set of services
    
    Returns:
        vm -- The generated vm
    """
    ip, mac = gen_rand_ip_and_mac(vms, number_of_vms, prefixe)

    v = vm.vm(ip, mac, behavior.behavior(ip + '/' + mac, services))
    for s in rand_services(services):
        v.add_service(s)

    return v


def prepare_vms(conf):
    """Prepares the vms all at once considering the given configuration
    
    Arguments:
        conf {dict} -- The configuration for the generated experiment
    
    Returns:
        list -- The list of vms generated
    """
    services = conf['network']['services']
    vms = list()

    number_of_vms = conf['network']['number_of_vms']
    for _ in range(conf['network']['number_of_changes'] * number_of_vms):
        vms += [gen_vm(vms, number_of_vms, conf['network']['prefixe'], services)]

    i = 0
    change_number = 0
    for v in vms:
        start = (
            0 if change_number == 0
            else change_number * number_of_vms
        )
        end = (
            ((change_number + 1) * number_of_vms) if ((change_number + 1) * number_of_vms) < len(vms)
            else len(vms)
        )
        actions = action_generator.generate(
            v, vms[start:end], conf, change_number, i)
        for a in actions:
            v.add_action(a)
        i += 1
        if int(i / number_of_vms) != change_number:
            change_number = int(i / number_of_vms)

    return vms


def write_data(vms, number_of_vms):
    """Writes the generated vms to disk
    
    Arguments:
        vms {list} -- The list of vms
        number_of_vms {int} -- The number of vms
    """
    csv = {'vm_number': [], 'change_number': []}
    i = 0
    for v in vms:
        for key, value in v.to_csv().items():
            if key in csv:
                csv[key] += [value]
            else:
                csv[key] = [value]
        csv['vm_number'] += [i % number_of_vms]
        csv['change_number'] += [int(i / number_of_vms)]
        i += 1

    df = pd.DataFrame(data=csv)

    keys = list(csv.keys())
    with open('vms/vms_list.csv', 'w') as f:
        df.to_csv(path_or_buf=f, sep=',', index=False,
                  columns=keys)

    keys.remove('vm_number')
    for i in range(number_of_vms):
        with open('vms/vm_' + str(i + 1) + '.csv', 'w') as f:
            machine = df[df['vm_number'] == i]
            machine.to_csv(path_or_buf=f, sep=',', index=False,
                           columns=keys)

    crontab_generator.generate(vms, number_of_vms)


def generate(conf, test):
    """Starts the vm generation and checks if it can do it
    
    Arguments:
        conf {dict} -- The configuration for this experiment
        test {boolean} -- True if we do not want to write the result to disk
    
    Raises:
        ValueError -- number of vms cannot be less than 2
        ValueError -- cannot have more machines than there is ip in range
    
    Returns:
        list -- The list of vms
    """
    if conf['network']['number_of_vms'] < 2:
        raise ValueError('number_of_vms cannot be less than 2')
    if conf['network']['number_of_vms'] > 252:
        raise ValueError('cannot have more machines than there is ip in range')

    vms = prepare_vms(conf)

    if not test:
        write_data(vms, conf['network']['number_of_vms'])

    return vms
