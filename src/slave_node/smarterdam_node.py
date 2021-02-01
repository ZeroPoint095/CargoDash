import canopen
import logging
import yaml
from time import sleep

'''
    We are not going to use this for the project but can be
    used for testing purposes.
'''


class SmarterdamSlaveNode:
    def __init__(self):
        with open('../config.yaml', 'r') as ymlfile:
            self.config = yaml.safe_load(ymlfile)
        self.selected_config = self.config['selected_config']
        # local node
        self.connectToNetwork(canopen.Network())
        self.network.create_node(3, '../eds_files/steering_node.eds')
        self.network.create_node(4, '../eds_files/motor_node.eds')
        while True:
            sleep(1)
            self.network.sync.transmit()

    def connectToNetwork(self, network):
        self.network = network
        try:
            bustype = self.config[self.selected_config]['bustype']
            channel = self.config[self.selected_config]['channel']
            bitrate = self.config[self.selected_config]['bitrate']
            network.connect(bustype=bustype, channel=channel, bitrate=bitrate)
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is set properly!'
                          f'(bustype = {bustype}, channel = {channel},'
                          f' bitrate = {bitrate})')


SmarterdamSlaveNode()
