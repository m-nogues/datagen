def create_machine(driver, machine):
    """
    Creates the machine as node in the graph
    :param driver: the driver of the graph database
    :param machine: the machine to create
    :return: the machine
    """
    num_packets = 0
    for rel in machine["relations"]:
        for port in machine["relations"][rel]:
            num_packets += machine["relations"][rel][port]
    with driver.session() as session:
        session.run('create (:Machine {{ip:\'{}\', total_pkt:\'{}\'}})'.format(machine["ip"], num_packets))
        session.close()
    return Machine(machine["ip"])


class Machine:
    def __init__(self, ip):
        self.__ip = ip

    def create_connection(self, driver, machine, port, rate):
        """
        Creates a connection between 2 machines with all the parameters it needs
        :param driver: the driver of the graph database
        :param machine: the machine to which the connection goes
        :param port: the port used during the communications
        :param rate: the number packets exchanged
        """
        with driver.session() as session:
            session.run('match (a:Machine), (b:Machine) where a.ip = \'{}\' and b.ip = \'{}\' create (a)-[r:EXCHANGED '
                        '{{port: \'{}\', rate:\'{:f}\'}}]->(b)'.format(self.ip, machine.ip, port, rate))
            session.close()

    # Attributes
    @property
    def ip(self): return self.__ip
