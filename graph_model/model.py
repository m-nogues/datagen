# driver = GraphDatabase.driver(
#    'bolt://localhost:7687', auth=('neo4j', 'iN2WuicrfZZ3s7d'))


def create_machine(driver, ip):
    with driver.session() as session:
        session.run('create (:Machine {{ip:\'{}\'}})'.format(ip))
        session.close()
    return Machine(ip)


class Machine:
    def __init__(self, ip):
        self.__ip = ip

    def create_connection(self, driver, machine, protocol, rate):
        with driver.session() as session:
            session.run('match (a:Machine), (b:Machine) where a.ip = \'{}\' and b.ip = \'{}\' create (a)-[r:EXCHANGED '
                        '{{protocol: \'{}\', rate:\'{:f}%\'}}]->(b)'.format(self.ip, machine.ip, protocol, rate))
            session.close()

    # Attributes
    @property
    def ip(self): return self.__ip
