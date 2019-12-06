#!/usr/bin/python
import argparse
import json
from datetime import datetime, timedelta

from modules.generators import hacker_generator, vm_generator
from modules.model import command, service


def configure(config_file):
    """Read the configuration file or creates the default one if it does not exist.

    Arguments:
        config_file {string} -- The configuration file

    Returns:
        dict -- The dictionnary containing the configuration
    """
    conf = {}
    try:
        with open(config_file, 'r') as f:
            conf = json.load(f)

        services = set()
        for s in conf['network']['services']:
            tmp = service.service(s['name'])
            for c in s['commands']:
                co = command.command(c['name'])
                for p in c['parameters']:
                    co.add_parameter(p)
                tmp.add_command(co)

            services.add(tmp)
        conf['network']['services'] = services

        attacks = set()
        for c in conf['hacker']['attacks']:
            co = command.command(c['name'])
            for p in c['parameters']:
                co.add_parameter(p)
            attacks.add(co)
        conf['hacker']['attacks'] = attacks

        conf['experiment']['start_date'] = datetime.strptime(
            conf['experiment']['start_date'], '%Y-%m-%d %H:%M')
        conf['experiment']['end_date'] = datetime.strptime(
            conf['experiment']['end_date'], '%Y-%m-%d %H:%M')
    except:
        conf['network'] = {
            'number_of_vms': 2,
            'number_of_changes': 1,
            'prefixe': '192.168.10.',
            'services': [
                {
                    'name': 'sshd',
                    'commands': [
                        {'name': '22', 'parameters': ['tester@&ip']},
                        {'name': 'sftp', 'parameters': ['tester@&ip']}
                    ]
                },
                {
                    'name': 'ftpd',
                    'commands': [
                        {'name': 'ftp', 'parameters': ['&ip']}
                    ]
                },
                {
                    'name': 'httpd',
                    'commands': [
                        {'name': 'wget', 'parameters': [
                            'http://&ip', '-r http://&ip']},
                        {'name': 'curl', 'parameters': ['http://&ip']}
                    ]
                }
            ]
        }
        conf['experiment'] = {
            'start_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'end_date': (datetime.now() + timedelta(7)).strftime('%Y-%m-%d %H:%M'),
            'max_actions_per_vm': 5
        }
        conf['hacker'] = {
            "attacks": [
                {
                    "name": "nmap",
                    "parameters": [
                        "&ip", "-sC 192.168.10.0/24", "-A 192.168.10.0/24", "-sV -F 192.168.10.0/24"
                    ]
                }
            ]
        }

        with open(config_file, 'w') as f:
            json.dump(conf, f)

        services = set()
        for s in conf['network']['services']:
            tmp = service.service(s['name'])
            for c in s['commands']:
                co = command.command(c['name'])
                for p in c['parameters']:
                    co.add_parameter(p)
                tmp.add_command(co)

            services.add(tmp)
        conf['network']['services'] = services

        conf['experiment']['start_date'] = datetime.strptime(
            conf['experiment']['start_date'], '%Y-%m-%d %H:%M')
        conf['experiment']['end_date'] = datetime.strptime(
            conf['experiment']['end_date'], '%Y-%m-%d %H:%M')

    return conf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Python framework for an easy creation of a network model for scientific pcap creation.')
    parser.add_argument('-c', '--conf', nargs='?', default='config.json',
                        help='specify an alternative configuration file')
    parser.add_argument('-t', '--test', action='store_true',
                        help='allows to run the framework without writing the outputs')

    args = parser.parse_args()

    conf = configure(args.conf)

    vms = vm_generator.generate(conf, args.test)

    hacker = hacker_generator.generate(vms, conf, args.test)

    if args.test:
        ret = 'vms:'
        i = 0
        for v in vms:
            ret += '\n\tvm_' + \
                str(i) + ':' + ''.join(['\n\t\t' +
                                        line for line in str(v).split('\n')])
            i += 1

        ret += '\nhacker:' + ''.join(['\n\t' +
                                      line for line in str(hacker).split('\n')])

        print(ret)
