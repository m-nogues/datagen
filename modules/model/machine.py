class machine:

    # Python native methods
    def __init__(self, ip, mac):
        self.__ip, self.__mac, self.__vms = ip, mac, set()

    def __str__(self):
        ret = 'ip:\t' + self.__ip + '\nmac:\t' + self.__mac + '\nvms:'
        i = 0
        for vm in sorted(self.__vms):
            ret += '\n\tvm_' + str(i) + ':' + ''.join(['\n\t\t' + line for line in str(vm).split('\n')])
            i += 1

        return ret

    # Attributes
    @property
    def ip(self): return self.__ip

    @property
    def mac(self): return self.__mac

    @property
    def vms(self): return self.__vms

    def add_vm(self, vm):
        try:
            self.__vms.add(vm)
        except:
            pass

    def del_vm(self, vm):
        try:
            self.__vms.remove(vm)
        except:
            pass

    # Useful methods
    def launch_vm(self, vm, declaration_csv):
        # TODO
        return