import can
import canopen
import logging
from threading import Thread

from listener.listener import Listener
from numpy import array, append, array2string, empty, set_printoptions
from canopen.sdo.exceptions import SdoCommunicationError


class CanOpenListener(Listener):
    ''' This class is being used to listen on a network and mainly
        tries to push the changes around other nodes to it's interpreter.
    '''
    def __init__(self, config, config_type='canopen_vcan', interpreter=None):
        ''' config : yaml_file_stream
                The configured yaml file that contains details for the
                connection type.

            config_type: string
                The selected configuration that is going to be used.
                The configurations are defined in 'config.yaml'.

            interpreter : CanOpenInterpreter
                The wanted interpreter that is going to be used.
        '''
        super().__init__(config)
        self.observers = array([])
        self.node_purposes = array([])
        self.config_type = config_type
        self.network = self.connect_to_network()
        self._add_nodes(self.config[self.config_type]['nodes'])
        self.interpreter = interpreter
        can_logging = self.config[self.config_type]['raw_can_data_logging']
        if(can_logging['enabled']):
            # Creates new network connection because CANopen library has
            # difficulties with multithreading on a single network connection.
            self.raw_log_network = self.connect_to_network()
            self.can_logging_buffer = can_logging['buffer']
            self.raw_data = empty([self.can_logging_buffer], dtype=can.Message)
            set_printoptions(threshold=self.can_logging_buffer)
            Thread(target=self._memorize_raw_data).start()

    def connect_to_network(self):
        ''' Connects to a can network.
            This method is depending on config.yaml, please
            configure the yaml file correctly before using this method.

            Returns canopen.Network.
        '''

        network = canopen.Network()
        try:
            bustype = self.config[self.config_type]['bustype']
            channel = self.config[self.config_type]['channel']
            bitrate = self.config[self.config_type]['bitrate']
            network.connect(bustype=bustype, channel=channel, bitrate=bitrate)
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is set properly!'
                          f'(bustype = {bustype}, channel = {channel},'
                          f' bitrate = {bitrate})')
        return network

    def listen_to_network(self):
        ''' Listens to connected network and tries to find any value changes
            within any connected node.
            The network sends out SDOs to be able to notice the value changes.

            Returns void.
        '''

        # Listens to every node
        for node_id in self.network:
            # Within a node find the variables saved
            for sdo_object in self.network[node_id].sdo.values():
                # And then get each variable's index and read it
                sdo_index = sdo_object.od.index
                try:
                    # Check for indices between 0x2000 and 0x5FFF
                    # Because we except communication between those
                    if (sdo_index >= 0x2000 and sdo_index <= 0x5FFF):
                        if (type(sdo_object) == canopen.sdo.base.Array
                           or type(sdo_object) == canopen.sdo.base.Record):
                            self._read_complex_variable(
                                self.network[node_id].sdo, sdo_index, node_id)
                        elif (type(sdo_object) == canopen.sdo.base.Variable):
                            self._read_simple_variable(
                                self.network[node_id].sdo, sdo_index, node_id)
                except SdoCommunicationError:
                    logging.error(f'The requested sdo ({hex(sdo_index)})'
                                  ' is not received!')

    def _read_complex_variable(self, sdo_client, sdo_index, node_id):
        for subindex in range(len(sdo_client[sdo_index]) + 1):
            # Skips subindex 0 because there are no value changes around this
            if(subindex != 0):
                index_and_subindex = f'{sdo_index}sub{subindex}'
                sdo_value = sdo_client.upload(sdo_index, subindex)
                # Checks for every subindex if value changed
                if(self._sdo_value_changed(index_and_subindex, sdo_value)):
                    self.inform_interpreter(sdo_value,
                                            sdo_client[sdo_index][subindex],
                                            node_id)

    def _read_simple_variable(self, sdo_client, sdo_index, node_id):
        sdo_value = sdo_client.upload(sdo_index, 0)
        if(self._sdo_value_changed(sdo_index, sdo_value)):
            self.inform_interpreter(sdo_value, sdo_client[sdo_index].od.name,
                                    node_id)

    def _add_nodes(self, nodes):
        for i in range(len(nodes)):
            self.node_purposes = append(
                self.node_purposes, nodes[i]['node_purpose'])
            # Either adds local or remote node bases on config for each node
            if(nodes[i]['local']):
                # Create a local node
                self.network.create_node(i + 1, nodes[i]['eds_location'])
            else:
                # Add a remote node
                self.network.add_node(i + 1, nodes[i]['eds_location'])

    def inform_interpreter(self, sdo_value, sdo_name, node_id):
        ''' Informs the interpreter with a changed SDO.

            sdo_value : any
                Sends out the changed value.

            sdo_name : canopen.sdo.Variable
                Sends out the changed SDO name.

            node_id : integer
                Used to read node purpose.

            Returns void.
        '''
        self.interpreter.inform_interpreter(sdo_value, sdo_name,
                                            self.node_purposes[node_id - 1])

    def set_interpreter(self, interpreter):
        ''' Set the interpreter where CanOpenListener can send messages to.

            interpreter : CanOpenInterpreter
                The wanted interpreter that is going to be used.

            Returns void.
        '''

        self.interpreter = interpreter

    def export_raw_can_data(self):
        ''' Exports raw can data at once. When this triggered the raw can data
            with the size of the buffer is exported. This can be used when an
            error/malfunction is occuring. 
        '''

        self.log_data(array2string(self.raw_data))

    def _sdo_value_changed(self, sdo_index, sdo_value):
        # Couldn't find a possibility to subscribe to a value with the CANopen
        # library, so needed to make an implementation by myself.

        found = False
        changed = False
        for observer in self.observers:
            if(observer['index'] == sdo_index):
                found = True
                if(observer['value'] != sdo_value):
                    observer['value'] = sdo_value
                    changed = True
        if(not found):
            self.observers = append(
                self.observers, {'index': sdo_index, 'value': sdo_value})
            changed = True
        return changed

    def _memorize_raw_data(self):
        # Uses circular buffer implementation.
        index = 0
        for raw_msg in self.raw_log_network.bus:
            index = (index + 1) % self.can_logging_buffer
            # If over buffer replace old data with new data.
            self.raw_data[index] = raw_msg
