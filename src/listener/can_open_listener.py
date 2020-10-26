import canopen
import yaml
import logging

from listener import Listener


class CanOpenListener(Listener):
    def __init__(self):
        super().__init__()
        self._load_configuration()
        self.connectToNetwork(canopen.Network())
        self.listenToNetwork()

    def connectToNetwork(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.cfg['canopen']['bustype'],
                                 channel=self.cfg['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')

    def listenToNetwork(self):
        for msg in self.network.bus:
            self.log_data(str(msg) + '\n')
            print(msg.data)

    def inform_interpreter(self):
        pass

    def _load_configuration(self):
        with open('../config.yaml', 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)


CanOpenListener()
