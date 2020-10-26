import canopen
import yaml
import logging

from listener import Listener


class CanOpenListener(Listener):
    def __init__(self):
        self._load_configuration()
        self.listenToNetwork(canopen.Network())
        super().__init__()

    def listenToNetwork(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.cfg['canopen']['bustype'],
                                 channel=self.cfg['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')

    def inform_interpreter(self):
        pass

    def _load_configuration(self):
        with open('../config.yaml', 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)


CanOpenListener()
