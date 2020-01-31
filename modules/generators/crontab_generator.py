import crontab as ct


def gen_cron(actions, cron):
    """Generate the crontab from the list of actions
    
    Arguments:
        actions {list} -- The list of actions
        cron {CronTab} -- The crontab to put the actions in
    
    Raises:
        AssertionError -- Raise an error if the job generated from an action is not valid.
    """
    for a in actions:
        job = cron.new(command=a.name + ' ' + a.parameters)
        job.setall(a.timestamp)
        if job.is_valid():
            job.enable()
        else:
            raise AssertionError('incorrect job from action:' + ''.join(['\n\t\t' +
                                                                         line for line in str(a).split('\n')]))


def write_data(crontabs, name='crontab'):
    """Writes the crontabs to disk
    
    Arguments:
        crontabs {list} -- The list of crontabs
    
    Keyword Arguments:
        name {str} -- The prefixe name of the files (default: {'crontab'})
    """
    for i in range(len(crontabs)):
        crontabs[i].write(filename='vms/' + name + '_' + str(i + 1))


def generate(vms, number_of_vms):
    """Writes the lists of actions of each vm to a crontab on the disk
    
    Arguments:
        vms {list} -- The list of vms to process
        number_of_vms {int} -- The number of physical vms
    """
    crontabs = [ct.CronTab() for _ in range(number_of_vms)]
    for i in range(len(vms)):
        gen_cron(vms[i].actions, crontabs[i % number_of_vms])

    write_data(crontabs)


def hacker(hacker):
    """Writes the list of actions of the hacker to a crontab on the disk
    
    Arguments:
        hacker {hacker} -- The hacker
    """
    crontab = ct.CronTab()
    gen_cron(hacker.actions, crontab)
    write_data([crontab], 'crontab_hacker')
