import random
from datetime import timedelta

from modules.model import action


def date_range(start, end):
    """Get a list of days in an interval
    
    Arguments:
        start {datetime} -- The starting day of the interval
        end {datetime} -- The ending day of the interval
    
    Returns:
        list -- The list of days
    """
    ret = []
    for n in range(int((end - start).days) + 1):
        ret += [start + timedelta(n)]

    return ret


def get_random_time_in_interval(interval, duration, start_date, change_number):
    """Get a random date in an interval
    
    Arguments:
        interval {list} -- The list of days representing the interval
        duration {timedelta} -- The duration of a configuration group
        start_date {datetime} -- The date, hour and minute of the start of the configuration group
        change_number {int} -- The number representing the configuration group
    
    Returns:
        datetime -- The chosen date, hour and minute
    """
    ret = random.choice(interval).replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59)
    )
    while ret > start_date + duration * (change_number + 1) or ret < start_date + duration * change_number:
        ret = random.choice(interval).replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59)
        )

    return ret


def format_parameter(parameter, vm):
    """Formats the parameter for a command
    
    Arguments:
        parameter {string} -- The parameter to format
        vm {vm} -- The VM targeted by the command
    
    Returns:
        string -- The formated parameter
    """
    ret = parameter.replace('&ip', vm.ip).replace('&mac', vm.mac)
    return ret


def get_random_action(vms, interval, duration, start_date, change_number):
    """Get a random action chosen in the range of possible actions
    
    Arguments:
        vms {list} -- A list of vms
        interval {list} -- A list of days representing the interval
        duration {timedelta} -- The duration of a configuration group
        start_date {datetime} -- The start date of the configuration group
        change_number {int} -- The number of the configuration group
    
    Returns:
        action -- The chosen action
    """
    rand_vm = random.choice(vms)
    rand_command = random.sample(random.sample(
        rand_vm.services, 1)[0].commands, 1)[0]

    rand_parameter = format_parameter(
        random.sample(rand_command.parameters, 1)[0], rand_vm)

    return action.action(rand_command.name, get_random_time_in_interval(interval, duration, start_date, change_number), rand_parameter)


def prepare_actions(vms, interval, max_actions, duration, start_date, change_number, index):
    """Generates a list of action for a vm of a configuration group
    
    Arguments:
        vms {list} -- The list of vms in the configuration group
        interval {list} -- The list of days in the interval
        max_actions {int} -- The maximum number of action to generate per vm
        duration {timedelta} -- The duration of a configuration group
        start_date {datetime} -- The start of the configuration group
        change_number {int} -- The number of the configuration group
        index {int} -- The index in the list of vms representing the vm for which we are generating the actions
    
    Returns:
        list -- The list of generated actions
    """
    actions = list()

    number_of_actions = random.randint(
        1, max_actions)
    while len(actions) < number_of_actions:
        actions += [get_random_action(vms, interval,
                                      duration, start_date, change_number)]

    actions += [action.action('/usr/local/bin/change_vm', start_date +
                              duration * change_number, '/vms/vm_' + str(((index + len(vms) + 1) % (len(vms) + 1)) + 1) + ' ' + str(change_number))]

    return actions


def generate(vm, vms, conf, change_number, index):
    """Prepares the parameters for the generation of actions
    
    Arguments:
        vm {vm} -- The vm for which to generate the actions
        vms {list} -- The list of vms in the configuration group
        conf {dict} -- The dictionnary containing the configuration parameters
        change_number {int} -- The number of the configuration group
        index {int} -- The index of the vm for which we generate the actions
    
    Returns:
        list -- The list of generated actions
    """
    duration = (conf['experiment']['end_date'] - conf['experiment']
                ['start_date']) / conf['network']['number_of_changes']

    interval = date_range(conf['experiment']['start_date'] + duration * change_number,
                          conf['experiment']['start_date'] + duration * (change_number + 1))

    vms.remove(vm)

    actions = prepare_actions(
        vms, interval, conf['experiment']['max_actions_per_vm'], duration, conf['experiment']['start_date'], change_number, index)

    return actions


def hacker(hacker, conf, vms):
    """The action generation for the hacker
    
    Arguments:
        hacker {hacker} -- The hacker
        conf {dict} -- The dictionnary containing the configuration parameters
        vms {list} -- The list of vms in the experiment
    
    Returns:
        list -- The list of generated actions
    """
    start_date = conf['experiment']['start_date']
    end_date = conf['experiment']['end_date']
    duration = (end_date - start_date) / conf['network']['number_of_changes']

    actions = list()
    number_of_actions = random.randint(
        1, conf['experiment']['max_actions_per_vm']) + 1
    actions += [action.action('/usr/local/bin/change_vm', start_date, '/vms/hacker 0')]
    
    while len(actions) < number_of_actions:
        index = random.randint(0, len(vms) - 1)
        rand_vm = vms[index]
        change_number = int(index/conf['network']['number_of_vms'])
        rand_command = random.sample(hacker.attacks, 1)[0]

        rand_parameter = format_parameter(
            random.sample(rand_command.parameters, 1)[0], rand_vm)

        interval = date_range(conf['experiment']['start_date'] + duration * change_number,
                              conf['experiment']['start_date'] + duration * (change_number + 1))

        a = action.action(rand_command.name, get_random_time_in_interval(
            interval, duration, start_date, change_number), rand_parameter)
        actions += [a]

    return actions
