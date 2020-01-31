class hacker:

    # Python native methods
    def __init__(self, ip, mac):
        self.__ip, self.__mac, self.__actions, self.__attacks, self.__started = ip, mac, set(), set(), False

    def __str__(self):
        ret = 'ip:\t' + self.__ip + '\nmac:\t' + self.__mac + '\nactions:'
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
    def actions(self): return self.__actions

    @property
    def attacks(self): return self.__attacks

    @property
    def started(self): return self.__started

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

    def add_attack(self, attack):
        try:
            self.__attacks.add(attack)
        except:
            pass

    def del_attack(self, attack):
        try:
            self.__attacks.remove(attack)
        except:
            pass

    # Useful methods
    def start(self):
        if not self.__started:
            # TODO
            self.__started = True
        return

    def stop(self):
        if self.__started:
            # TODO
            self.__started = False
        return

    def to_csv(self):
        ret = {
            'ip': self.__ip,
            'mac': self.__mac,
            'actions': ';'.join([action.name + ',' + str(action.timestamp) + ',' + action.parameters for action in self.__actions])
        }
        return ret
