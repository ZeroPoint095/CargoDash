import canopen
import logging

from listener.listener import Listener
from canopen.sdo.exceptions import SdoCommunicationError


class CanOpenListener(Listener):
    ''' This class is being used to listen on a network and mainly
        tries to push the changes around other nodes to it's interpreter.
    '''
    def __init__(self, config, interpreter=None):
        ''' config : yaml_file_stream
                The configured yaml file that contains details for the
                connection type.
            interpreter : CanOpenInterpreter
                The wanted interpreter that is going to be used.
        '''
        super().__init__(config)
        self.observers = []
        self.connect_to_network()
        self._add_nodes(self.config['canopen']['nodes'])
        self.interpreter = interpreter

    def connect_to_network(self):
        ''' Connects to a can network.
            This method is depending on config.yaml, please
            configure the yaml file correctly before using this method.

            Returns void.
        '''

        self.network = canopen.Network()
        try:
            self.network.connect(bustype=self.config['canopen']['bustype'],
                                 channel=self.config['canopen']['channel'])
        except OSError:
            logging.error('CanOpenListener is unable to listen to network,'
                          ' please check if configuration is setted properly!')

    def listen_to_network(self):
        ''' Listens to connected network and tries to find any value changes.
            The network sends out SDOs to be able to notice this.

            Returns void.
        '''

        # Listens to every node
        for node_id in self.network:
            # Within a node find the variables saved
            for sdo_object in self.network[node_id].sdo.values():
                # And then get each variable's index and read it
                sdo_index = sdo_object.od.index
                try:
                    # TODO: Only allows simple variables for now, 
                    #        needs to be able process complex variables.
                    sdo_value = self.network[node_id].sdo.upload(
                                sdo_index, 0)
                    if(self._sdo_value_changed(sdo_index, sdo_value)):
                        self.inform_interpreter(sdo_index)
                except SdoCommunicationError:
                    logging.error(f'The requested sdo ({hex(sdo_index)})'
                                  ' is not received')

    def inform_interpreter(self, sdo_object):
        ''' Informs the interpreter with a changed SDO.

            sdo_object : canopen.sdo.Variable
                Sends out the changed SDO.
        
            Returns void.
        '''

        self.interpreter.inform_interpreter(sdo_object)

    def set_interpreter(self, interpreter):
        ''' Set the interpreter where CanOpenListener can send messages to.

            interpreter : CanOpenInterpreter
                The wanted interpreter that is going to be used.

            Returns void.
        '''

        self.interpreter = interpreter

    def _add_nodes(self, nodes):
        for i in range(len(nodes)):
            # Either adds local or remote node bases on config for each node
            if (nodes[i]['local']):
                self.network.create_node(i + 1, nodes[i]['eds_location'])
            else:
                self.network.add_node(i + 1, nodes[i]['eds_location'])

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
