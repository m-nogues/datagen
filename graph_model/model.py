# driver = GraphDatabase.driver(
#    'bolt://localhost:7687', auth=('neo4j', 'iN2WuicrfZZ3s7d'))


def create_machine(driver, machine):
    """
    Creates the machine as node in the graph
    :param driver: the driver of the graph database
    :param machine: the machine to create
    :return: the machine
    """
    num_packets = 0
    for rel in machine["relations"]:
        for prot in machine["relations"][rel]:
            num_packets += machine["relations"][rel][prot]
    with driver.session() as session:
        session.run('create (:Machine {{ip:\'{}\', total_pkt:\'{}\'}})'.format(machine["ip"], num_packets))
        session.close()
    return Machine(machine["ip"])


class Machine:
    def __init__(self, ip):
        self.__ip = ip

    def create_connection(self, driver, machine, protocol, rate):
        """
        Creates a connection between 2 machines with all the parameters it needs
        :param driver: the driver of the graph database
        :param machine: the machine to which the connection goes
        :param protocol: the protocol
        :param rate:
        """
        with driver.session() as session:
            session.run('match (a:Machine), (b:Machine) where a.ip = \'{}\' and b.ip = \'{}\' create (a)-[r:EXCHANGED '
                        '{{protocol: \'{}\', rate:\'{:f}\'}}]->(b)'.format(self.ip, machine.ip, protocol, rate))
            session.close()

    # Attributes
    @property
    def ip(self): return self.__ip
