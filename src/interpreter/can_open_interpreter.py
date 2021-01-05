from interpreter.interpreter import Interpreter
from node_input_factory.node_input_factory import NodeInputFactory
from node_input_factory.node_input_enums import NodeType
from struct import unpack


class CanOpenInterpreter(Interpreter):
    def __init__(self, vehicle):
        self.node_input_factory = NodeInputFactory()
        self.vehicle = vehicle
        super().__init__()

    def inform_interpreter(self, sdo_value, sdo_name, sdo_data_type,
                           node_properties, index, sub_index):
        ''' This method is requested by the CanOpenListener when it notices
            changes at a certain sdo value.

            sdo_value: any
                Value to change the state of the vehicle.

            sdo_name: string
                The name of the SDO.

            sdo_data_type:
                The data_type as string representing a
                hexadecimal value.

            node_properties: dictionary {name: string, type: integer}
                A dictionary that contains a name/description about the node
                and the type of the node.

            index : string
                Index of the variable.

            sub_index : string
                Sub-index of the variable.

            Returns void.
        '''
        self._interpret_object(sdo_value, sdo_name,
                               sdo_data_type,
                               node_properties['name'],
                               node_properties['type'],
                               index, sub_index)

    def _interpret_object(self, value, name, sdo_data_type, node_name,
                          node_type_index, index, sub_index):
        node_type = NodeType(node_type_index)
        unpack_format = self._get_unpack_format(sdo_data_type)
        # Checks every possible node
        if(NodeType.DistanceNode == node_type):
            # Adding index, sub_index as additional attributes.
            n_input = self.node_input_factory.create_distance_node_input(
                unpack(unpack_format, value)[0], name, node_name, index=index,
                sub_index=sub_index, data_type=sdo_data_type)
        elif(NodeType.SteeringNode == node_type):
            n_input = self.node_input_factory.create_steering_node_input(
                unpack(unpack_format, value)[0], name, node_name, index=index,
                sub_index=sub_index, data_type=sdo_data_type)
        elif(NodeType.LocalizationNode == node_type):
            n_input = self.node_input_factory.create_localization_node_input(
                value, name, node_name, index=index,
                sub_index=sub_index, data_type=sdo_data_type)
        elif(NodeType.EngineNode == node_type):
            value_to_bool = True if (
                unpack(unpack_format, value)[0]) == 1 else False
            n_input = self.node_input_factory.create_engine_node_input(
                value_to_bool, name, node_name, index=index,
                sub_index=sub_index)
        else:
            n_input = self.node_input_factory.create_temperature_node_input(
                unpack(unpack_format, value)[0], name, node_name, index=index,
                sub_index=sub_index, data_type=sdo_data_type)
        self.vehicle.edit_vehicle_state(n_input)

    def _get_unpack_format(self, can_open_data_type):
        result = ''

        data_types = {'0x1': 'c', '0x2': 'b', '0x3': 'h', '0x4': 'i',
                      '0x15': 'q', '0x5': 'B', '0x6': 'H', '0x7': 'I',
                      '0x1B': 'Q', '0x8': 'f', '0x11': 'd'}
        try:
            result = data_types[can_open_data_type]
        except KeyError:
            print(f'Data type {can_open_data_type} is not supported!')

        return result
