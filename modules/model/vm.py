from modules.model import behavior


class vm:

    # Python native methods
    def __init__(self, ip, mac, behavior):
        self.__ip, self.__mac, self.__services, self.__behavior, self.__actions, self.__started = ip, mac, set(
        ), behavior, set(), False

    def __str__(self):
        ret = 'ip:\t' + self.__ip + '\nmac:\t' + self.__mac + '\nservices:'
        i = 0
        for service in self.__services:
            ret += '\n\tservice_' + \
                str(i) + ':' + ''.join(['\n\t\t' + 
                                        line for line in str(service).split('\n')])
            i += 1

        ret += '\nbehavior:' + ''.join(['\n\t' + 
                                        line for line in str(self.__behavior).split('\n')]) + '\nactions:'
        i = 0
        for action in self.__actions:
            ret += '\n\taction_' + \
                str(i) + ':' + ''.join(['\n\t\t' + 
                                        line for line in str(action).split('\n')])
            i += 1

        return ret

    # Attributes
    @property
    def ip(self): return self.__ip

    @property
    def mac(self): return self.__mac

    @property
    def services(self): return self.__services

    @property
    def behavior(self): return self.__behavior

    @property
    def actions(self): return self.__actions

    @property
    def started(self): return self.__started

    def add_service(self, service):
        try:
            self.__services.add(service)
        except:
            pass

    def del_service(self, service):
        try:
            self.__services.remove(service)
        except:
            pass

    def update_behavior(self, service, bias):
        self.__behavior.change_bias((service, bias))

    def add_action(self, action):
        try:
            self.__actions.add(action)
        except:
            pass

    def del_action(self, action):
        try:
            self.__actions.remove(action)
        except:
            pass

    # Useful methods
    def start(self):
        if not self.__started:
            # TODO
            for service in self.__services:
                service.start()
            self.__started = True
        return

    def stop(self):
        if self.__started:
            # TODO
            for service in self.__services:
                service.stop()
            self.__started = False
        return

    def to_csv(self):
        ret = {
            'ip': self.__ip,
            'mac': self.__mac,
            'services': ' '.join([service.name for service in self.__services]),
            'behavior': self.__behavior.name,
            'actions': ';'.join([action.name + ',' + str(action.timestamp) + ',' + action.parameters for action in self.__actions])
        }
        return ret
