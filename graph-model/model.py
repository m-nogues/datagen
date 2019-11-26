# driver = GraphDatabase.driver(
#    'bolt://localhost:7687', auth=('neo4j', 'iN2WuicrfZZ3s7d'))


class Machine:
    def __init__(self, name, ip):
        self.__name, self.__ip = name, ip

    def create_machine(driver, name, ip):
        with driver.session() as session:
            session.run('create (' + name + ':Machine {name:\'' + name
                        + '\', ip:\'' + ip + '\'})')
            session.close()
        return Machine(name, ip)

    def create_connection(self, driver, machine, protocol, rate):
        with driver.session() as session:
            session.run('match (a:Machine), (b:Machine) where a.name = \''
                        + self.__name + '\' and b.name = \''
                        + machine.name +
                        '\' create (a)-[r:EXCHANGED {protocol: \''
                        + protocol + '\', rate:\'' + str(rate) + '%\'}]->(b)')
            session.close()

    # Attributes
    @property
    def name(self): return self.__name

    @property
    def ip(self): return self.__ip
