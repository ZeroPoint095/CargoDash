from interpreter.interpreter import Interpreter
from node_input_factory.node_input_factory import NodeInputFactory
from node_input_factory.node_input_enums import NodeType
from struct import unpack


class CanOpenInterpreter(Interpreter):
    def __init__(self, vehicle):
        self.node_input_factory = NodeInputFactory()
        self.vehicle = vehicle
        super().__init__()

    def inform_interpreter(self, node_data):
        ''' This method is requested by the CanOpenListener when it notices
            changes at a certain sdo value.

            node_data:
                Contains the current state information of a sensor/actuator
                , it's addresses and naming.

            Returns void.
        '''
        self._interpret_object(node_data)

    def _interpret_object(self, node_data):
        node_type = NodeType(node_data['node_type_index'])
        unpack_format = self._get_unpack_format(node_data['sdo_data_type'])
        # Checks every possible node
        if(NodeType.DistanceNode == node_type):
            # Adding index, sub_index as additional attributes.
            n_input = self.node_input_factory.create_distance_node_input(
                unpack(unpack_format, node_data['sdo_value'])[0],
                node_data['sdo_name'], node_data['node_name'],
                index=node_data['index'],
                sub_index=node_data['sub_index'],
                data_type=node_data['sdo_data_type'],
                access_type=node_data['access_type'],
                parent_name=node_data['parent_name'])
        elif(NodeType.SteeringNode == node_type):
            n_input = self.node_input_factory.create_steering_node_input(
                unpack(unpack_format, node_data['sdo_value'])[0],
                node_data['sdo_name'], node_data['node_name'],
                index=node_data['index'],
                sub_index=node_data['sub_index'],
                data_type=node_data['sdo_data_type'],
                access_type=node_data['access_type'],
                parent_name=node_data['parent_name'])
        elif(NodeType.LocalizationNode == node_type):
            n_input = self.node_input_factory.create_localization_node_input(
                unpack(unpack_format, node_data['sdo_value'])[0],
                node_data['sdo_name'], node_data['node_name'],
                index=node_data['index'],
                sub_index=node_data['sub_index'],
                data_type=node_data['sdo_data_type'],
                access_type=node_data['access_type'],
                parent_name=node_data['parent_name'])
        elif(NodeType.EngineNode == node_type):
            n_input = self.node_input_factory.create_engine_node_input(
                unpack(unpack_format, node_data['sdo_value'])[0],
                node_data['sdo_name'], node_data['node_name'],
                index=node_data['index'],
                sub_index=node_data['sub_index'],
                data_type=node_data['sdo_data_type'],
                access_type=node_data['access_type'],
                parent_name=node_data['parent_name'])
        else:
            n_input = self.node_input_factory.create_temperature_node_input(
                unpack(unpack_format, node_data['sdo_value'])[0],
                node_data['sdo_name'], node_data['node_name'],
                index=node_data['index'],
                sub_index=node_data['sub_index'],
                data_type=node_data['sdo_data_type'],
                access_type=node_data['access_type'],
                parent_name=node_data['parent_name'])
        self.vehicle.edit_vehicle_state(n_input)

    def _get_unpack_format(self, can_open_data_type):
        result = ''

        data_types = {'0x1': 'b', '0x2': 'b', '0x3': 'h', '0x4': 'i',
                      '0x15': 'q', '0x5': 'B', '0x6': 'H', '0x7': 'I',
                      '0x1B': 'Q', '0x8': 'f', '0x11': 'd'}
        try:
            result = data_types[can_open_data_type]
        except KeyError:
            print(f'Data type {can_open_data_type} is not supported!')

        return result
