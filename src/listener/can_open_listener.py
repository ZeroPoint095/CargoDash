import canopen
import logging

from time import sleep
from listener.listener import Listener
from canopen.sdo.exceptions import SdoCommunicationError


class CanOpenListener(Listener):
    def __init__(self, config):
        super().__init__(config)
        self.observers = []
        self.connect_to_network(canopen.Network())
        self.add_nodes(self.config['canopen']['nodes'])
        self.listen_to_network()

    def connect_to_network(self, network):
        self.network = network
        try:
            self.network.connect(bustype=self.config['canopen']['bustype'],
                                 channel=self.config['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')

    def add_nodes(self, nodes):
        for i in range(len(nodes)):
            # Either adds local or remote node bases on config for each node
            if (nodes[i]['local']):
                self.network.create_node(i + 1, nodes[i]['eds_location'])
            else:
                self.network.add_node(i + 1, nodes[i]['eds_location'])

    def listen_to_network(self):
        while True:
            sleep(0.1)
            # Listens to every node
            for node_id in self.network:
                # Within a node find the variables saved
                for sdo_object in self.network[node_id].sdo.values():
                    # And then get each variable's index and read it
                    sdo_index = sdo_object.od.index
                    try:
                        # Only allows simple variables for now
                        sdo_value = self.network[node_id].sdo.upload(
                                    sdo_object.od.index, 0)
                        if(self._sdo_value_changed(sdo_index, sdo_value)):
                            self.inform_interpreter(sdo_index)
                    except SdoCommunicationError:
                        logging.error('The requested node doesn\'t'
                                      ' give a response')

    def inform_interpreter(self, can_id):
        print(can_id)

    def _sdo_value_changed(self, sdo_index, sdo_value):
        # Couldn't find a possibility to subscribe to a value with the CANopen
        # library, so needed to make an implementation by myself.
        found = False
        changed = False
        for observer in self.observers:
            if(observer['index'] == sdo_index):
                found = True
                if (observer['value'] != sdo_value):
                    observer['value'] = sdo_value
                    changed = True
        if (not found):
            self.observers.append({'index': sdo_index, 'value': sdo_value})
            changed = True
        return changed
