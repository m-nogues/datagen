class action:

    # Python native methods
    def __init__(self, name, timestamp, parameters):
        self.__name, self.__timestamp, self.__parameters = name, timestamp, parameters

    def __str__(self):
        return 'type:\t' + self.__name + '\ntimestamp:\t' + str(self.__timestamp) + '\nparameters:\t' + self.__parameters + '\n'

    # Attributes
    @property
    def name(self): return self.__name

    @property
    def timestamp(self): return self.__timestamp

    @property
    def parameters(self): return self.__parameters

    # Useful methods
    def execute(self):
        # TODO
        return
