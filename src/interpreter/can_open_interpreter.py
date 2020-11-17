from interpreter.interpreter import Interpreter
from node_input_factory.node_input_factory import NodeInputFactory
from node_input_factory.node_input_enums import NodeType
from struct import unpack


class CanOpenInterpreter(Interpreter):
    def __init__(self, vehicle):
        self.node_input_factory = NodeInputFactory()
        self.vehicle = vehicle
        super().__init__()

    def inform_interpreter(self, sdo_value, sdo_name, node_purpose):
        ''' This method is requested by the CanOpenListener when it notices
            changes at a certain sdo value.

            sdo_value: any
                Value to change the state of the vehicle.

            sdo_object: string
                The name of the SDO.

            node_purpose: dictionary {name: string, type: integer}
                A dictionary that contains a name/description about the node
                and the type of the node.

            Returns void.
        '''
        self._interpret_object(sdo_value, sdo_name,
                               node_purpose['name'], node_purpose['type'])

    def _interpret_object(self, value, name, node_name, node_type_index):
        node_type = NodeType(node_type_index)
        # Checks every possible node
        if(NodeType.DistanceNode == node_type):
            n_input = self.node_input_factory.create_distance_node_input(
                unpack('h', value)[0], name, node_name)
        elif(NodeType.SteeringNode == node_type):
            n_input = self.node_input_factory.create_steering_node_input(
                unpack('h', value)[0], name, node_name)
        elif(NodeType.LocalizationNode == node_type):
            n_input = self.node_input_factory.create_localization_node_input(
                value, name, node_name)
        elif(NodeType.EngineNode == node_type):
            value_to_bool = True if unpack('h', value)[0] == 1 else False
            n_input = self.node_input_factory.create_engine_node_input(
                value_to_bool, name, node_name)
        else:
            n_input = self.node_input_factory.create_temperature_node_input(
                unpack('h', value)[0], name, node_name)
        self.vehicle.edit_vehicle_state(n_input)
