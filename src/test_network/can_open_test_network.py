import canopen
import can
import logging
import time
from test_network.test_network import TestNetwork


class CanOpenTestNetwork(TestNetwork):
    def __init__(self, config, config_type='canopen_vcan'):
        super().__init__(config, config_type)

    def connected_to_network(self):
        ''' Connects to a can network.
            This method is depending on config.yaml, please
            configure the yaml file correctly before using this method.

            Returns boolean.
        '''
        connected = True
        self.network = canopen.Network()
        try:
            bustype = self.config[self.config_type]['bustype']
            channel = self.config[self.config_type]['channel']
            bitrate = self.config[self.config_type]['bitrate']
            self.network.connect(bustype=bustype, channel=channel,
                                 bitrate=bitrate)
            self._add_nodes(self.config[self.config_type]['nodes'])
        except OSError:
            connected = False
            logging.error('CanOpenTestNetwork is unable to listen to network,'
                          ' please check if configuration is set properly!'
                          f'(bustype = {bustype}, channel = {channel},'
                          f' bitrate = {bitrate})')
        return connected

    def _add_nodes(self, nodes):
        for i in range(len(nodes)):
            # Either adds local or remote node bases on config for each node
            if(nodes[i]['local']):
                # Create a local node
                self.network.create_node(nodes[i]['node_properties']['id'],
                                         nodes[i]['eds_location'])
            else:
                # Add a remote node
                self.network.add_node(nodes[i]['node_properties']['id'],
                                      nodes[i]['eds_location'])

    def test_connection(self):
        try:
            self.network.scanner.search()
            time.sleep(2)
        except can.CanError:
            logging.error("CAN network is down!")

        for node_id in self.network:
            if(node_id not in self.network.scanner.nodes):
                logging.error(
                    f'Node {node_id} not found on CANBUS (No heartbeat). '
                    'Please check connections or master/node EDS')

        for node_id in self.network.scanner.nodes:
            if node_id not in self.network.nodes:
                logging.warning(f'Node {node_id} found on CANBUS,'
                                'but not registered to network.')

        for node_id in self.network.scanner.nodes:
            if node_id in self.network.nodes:
                logging.info(f'Node {node_id} found on CANBUS'
                             'and registered to network.')
