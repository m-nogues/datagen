class service:

    # Python native methods
    def __init__(self, name):
        self.__name, self.__commands, self.__started = name, set(), False

    def __str__(self):
        ret = 'name:\t' + self.__name + '\ncommands:'
        i = 0
        for command in self.__commands:
            ret += '\n\tcommand_' + str(i) + ':' + ''.join(['\n\t\t' +
                                                            line for line in str(command).split('\n')])
            i += 1

        return ret

    # Attributes
    @property
    def name(self): return self.__name

    @property
    def commands(self): return self.__commands

    @property
    def started(self): return self.__started

    def add_command(self, command):
        try:
            self.__commands.add(command)
        except:
            print('Error while adding the command')
            pass

    def del_command(self, command):
        try:
            self.__commands.remove(command)
        except:
            print('Error while deleting the command')
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
