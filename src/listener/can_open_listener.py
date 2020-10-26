import canopen
import logging

from listener.listener import Listener


class CanOpenListener(Listener):
    def __init__(self, config):
        super().__init__(config)
        self.connectToNetwork(canopen.Network())
        self.listenToNetwork()

    def connectToNetwork(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.config['canopen']['bustype'],
                                 channel=self.config['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')

    def listenToNetwork(self):
        for msg in self.network.bus:
            self.log_data(str(msg) + '\n')

    def inform_interpreter(self):
        pass
