from datetime import datetime, timedelta
from django.db import models

# Create your models here.


class Parameter(models.Model):
    name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(unique=True, max_length=200)
    timestamp = models.DateTimeField('timestamp')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)

    def __str__(self):
        return 'type:\t' + self.name + '\ntimestamp:\t' + str(self.timestamp) + '\nparameters:\t' + str(self.parameter) + '\n'


class Command(models.Model):
    name = models.CharField(max_length=200)
    parameters = models.ManyToManyField(Parameter, blank=True)

    def __str__(self):
        ret = 'name:\t' + self.name + '\nparameters:' + \
            ''.join(['\n\t' + str(p) for p in self.parameters.all()])
        return ret


class Service(models.Model):
    name = models.CharField(unique=True, max_length=200)
    commands = models.ManyToManyField(Command)

    def __str__(self):
        ret = 'name:\t' + self.name + '\ncommands:'
        i = 0
        for command in self.commands.all():
            ret += '\n\tcommand_' + str(i) + ':' + ''.join(['\n\t\t' +
                                                            line for line in str(command).split('\n')])
            i += 1
        return ret


class Attack(models.Model):
    name = models.CharField(max_length=200)
    parameters = models.ManyToManyField(Parameter)

    def __str__(self):
        ret = 'name:\t' + self.name + '\nparameters:' + \
            ''.join(['\n\t' + str(p) for p in self.parameters.all()])
        return ret


class Bias(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    bias = models.FloatField()

    def __str__(self):
        return self.service.name + ':\t' + str(self.bias)


class Behavior(models.Model):
    name = models.CharField(unique=True, max_length=200)
    bias = models.ManyToManyField(Bias)

    def __str__(self):
        ret = 'name:\t' + self.name + '\nbias:'

        for b in self.bias.all():
            ret += '\n\t' + str(b)
        return ret


class Hacker(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    mac = models.CharField(unique=True, max_length=200)
    actions = models.ManyToManyField(Action, blank=True)
    attacks = models.ManyToManyField(Attack)

    def __str__(self):
        ret = 'ip:\t' + self.ip + '\nmac:\t' + self.mac + '\nactions:'
        i = 0
        for action in self.actions.all():
            ret += '\n\taction_' + \
                str(i) + ':' + ''.join(['\n\t\t' +
                                        line for line in str(action).split('\n')])
            i += 1
        return ret

    def to_csv(self):
        ret = {
            'ip': self.ip,
            'mac': self.mac,
            'actions': ';'.join([action.name + ',' + str(action.timestamp) + ',' + action.parameters for action in self.actions.all()])
        }
        return ret


class Vm(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    mac = models.CharField(unique=True, max_length=200)
    services = models.ManyToManyField(Service)
    behavior = models.ForeignKey(Behavior, on_delete=models.CASCADE)
    actions = models.ManyToManyField(Action, blank=True)

    def __str__(self):
        ret = 'ip:\t' + self.ip + '\nmac:\t' + self.mac + '\nservices:'
        i = 0
        for service in self.services.all():
            ret += '\n\tservice_' + \
                str(i) + ':' + ''.join(['\n\t\t' +
                                        line for line in str(service).split('\n')])
            i += 1

        ret += '\nbehavior:' + ''.join(['\n\t' +
                                        line for line in str(self.behavior).split('\n')]) + '\nactions:'
        i = 0
        for action in self.actions.all():
            ret += '\n\taction_' + \
                str(i) + ':' + ''.join(['\n\t\t' +
                                        line for line in str(action).split('\n')])
            i += 1
        return ret

    def to_csv(self):
        ret = {
            'ip': self.ip,
            'mac': self.mac,
            'services': ' '.join([service.name for service in self.services.all()]),
            'behavior': self.behavior.name,
            'actions': ';'.join([action.name + ',' + str(action.timestamp) + ',' + str(action.parameter) for action in self.actions.all()])
        }
        return ret


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    network = models.GenericIPAddressField(default='192.168.10.0')
    started = models.BooleanField(default=False)

    nb_vms = models.IntegerField('nombre de vms', default=4)
    nb_hackers = models.IntegerField('nombre de hackers', default=1)
    max_actions = models.IntegerField('nombre d\'actions maximum par vms', default=500)

    start_date = models.DateTimeField(
        'start', default=datetime.now() + timedelta(hours=1))
    end_date = models.DateTimeField(
        'end', default=datetime.now() + timedelta(hours=5))

    hackers = models.ManyToManyField(Hacker, blank=True)
    vms = models.ManyToManyField(Vm, blank=True)

    def __str__(self):
        ret = 'name:\t' + self.name + '\nvms:'
        i = 0
        for vm in self.vms.all():
            ret += '\n\tvm_' + \
                str(i) + ':' + ''.join(['\n\t\t' +
                                        line for line in str(vm).split('\n')])
            i += 1

        i = 0
        ret += '\nhackers:'
        for hacker in self.hackers.all():
            ret += '\n\thacker_' + \
                str(i) + ':' + ''.join(['\n\t\t' +
                                        line for line in str(hacker).split('\n')])
            i += 1
        return ret
