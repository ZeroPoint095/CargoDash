import canopen
import logging
import yaml
from time import sleep

'''
    We are not going to use this for the project but can be
    used for testing purposes.
'''


class MeasuringSlaveNode:
    def __init__(self):
        with open('../config.yaml', 'r') as ymlfile:
            self.config = yaml.safe_load(ymlfile)
        # local node
        self.connectToNetwork(canopen.Network())
        self.network.create_node(1, '../eds_files/measuring_distance_node.eds')
        while True:
            sleep(1)
            print(self.network[1].sdo[0x2000].phys)
            self.network[1].sdo.download(0x2000, 0, bytes(
                [self.network[1].sdo[0x2000].phys + 1, 0]))
            self.network.sync.transmit()

    def connectToNetwork(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.config['canopen_vcan']['bustype'],
                                 channel=self.config['canopen_vcan']['channel'],
                                 bitrate=self.config['canopen_vcan']['bitrate'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')


MeasuringSlaveNode()
