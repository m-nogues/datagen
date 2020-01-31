class behavior:

    # Python native methods
    def __init__(self, name, services):
        self.__name, self.__bias = name, dict()
        for s in services:
            self.__bias[s.name] = 1 / len(services)

    def __str__(self):
        ret = 'name:\t' + self.__name + '\nbias:'

        for key, value in self.__bias.items():
            ret += '\n\t' + key + ':\t' + str(value)

        return ret

    # Attributes
    @property
    def name(self): return self.__name

    @property
    def bias(self): return self.__bias

    def change_bias(self, key, value):
        if not isinstance(value, float) or value > 1.0 or value < 0.0:
            raise TypeError('value must be between 0.0 and 1.0')
        if key in self.__bias:
            self.__bias[key] = value
        else:
            raise KeyError(key + ' is not a valid service')

    def get_bias(self, key):
        if key in self.__bias:
            return self.__bias[key]
        else:
            raise KeyError(key + ' is not a valid service')

    # Useful methods
