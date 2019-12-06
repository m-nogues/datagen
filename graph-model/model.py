# driver = GraphDatabase.driver(
#    'bolt://localhost:7687', auth=('neo4j', 'iN2WuicrfZZ3s7d'))


def create_machine(driver, ip):
    with driver.session() as session:
        session.run('create (' + ip + ':Machine {ip:\'' + ip + '\'})')
        session.close()
    return Machine(ip)


class Machine:
    def __init__(self, ip):
        self.__ip = ip

    def create_connection(self, driver, machine, protocol, rate):
        with driver.session() as session:
            session.run('match (a:Machine), (b:Machine) where a.ip = \''
                        + self.__ip + '\' and b.ip = \''
                        + machine.ip +
                        '\' create (a)-[r:EXCHANGED {protocol: \''
                        + protocol + '\', rate:\'' + str(rate) + '%\'}]->(b)')
            session.close()

    # Attributes
    @property
    def ip(self): return self.__ip
