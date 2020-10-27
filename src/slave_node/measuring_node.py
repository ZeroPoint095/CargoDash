import canopen
import logging
import yaml
from time import sleep


class MeasuringSlaveNode:
    def __init__(self):
        with open('../config.yaml', 'r') as ymlfile:
            self.config = yaml.safe_load(ymlfile)
        self.connectToNetwork(canopen.Network())
        od = canopen.ObjectDictionary()
        variable = canopen.objectdictionary.Variable(
                   'Measuring distance', 0x2000)
        variable.data_type = canopen.objectdictionary.UNSIGNED16
        variable.access_type = 'rw'
        variable.value = 0x6
        od.add_object(variable)
        self.network.create_node(1, od)
        while True:
            sleep(1)
            print(self.network[1].sdo[0x2000].phys)
            self.network.sync.transmit()
            

    def connectToNetwork(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.config['canopen']['bustype'],
                                 channel=self.config['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')


MeasuringSlaveNode() 