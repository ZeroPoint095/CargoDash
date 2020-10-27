import canopen
import logging

from listener.listener import Listener


class CanOpenListener(Listener):
    def __init__(self, config, nodes):
        super().__init__(config)
        self.connectToNetwork(canopen.Network())
        self.addNodes(nodes)
        self.listenToNetwork()

    def connectToNetwork(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.config['canopen']['bustype'],
                                 channel=self.config['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')

    def addNodes(self, nodes):
        for i in range(len(nodes)):
            od = canopen.ObjectDictionary()
            variable = canopen.objectdictionary.Variable(
                       'Measuring distance', 0x2000)
            variable.data_type = canopen.objectdictionary.UNSIGNED16
            variable.access_type = 'rw'
            od.add_object(variable)
            self.network.add_node(i + 1, od)

    def listenToNetwork(self):
        for node_id in self.network:
            self.network[node_id].sdo.upload(0x2000, 0)
            number = self.network[node_id].sdo[0x2000].phys
            print(bytes([number, 0]))
            self.network[node_id].sdo.download(0x2000, 0,
                                               bytes([number + 1, 0]))

    def inform_interpreter(self):
        pass
