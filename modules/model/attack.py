class attack:

    # Python native methods
    def __init__(self, service):
        self.__service, self.__commands = service, set()

    def __str__(self):
        ret = 'service:\n'+''.join(['\n\t\t' +
                                    line for line in str(self.__service).split('\n')])+'\ncommands:'
        i = 0
        for command in self.__commands:
            ret += '\n\tcommand_' + str(i) + ':' + ''.join(['\n\t\t' +
                                                            line for line in str(command).split('\n')])
            i += 1

        return ret

    # Attributes
    @property
    def service(self): return self.__service

    @property
    def commands(self): return self.__commands

    def add_command(self,command):
        try:
            self.__commands.add(command)
        except:
            pass
    
    def del_command(self,command):
        try:
            self.__commands.remove(command)
        except:
            pass

    # Useful methods
