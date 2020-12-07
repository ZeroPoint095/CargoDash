from node_input_factory.node_input_classes import (DistanceNodeInput,
                                                   SteeringNodeInput,
                                                   LocalizationNodeInput,
                                                   EngineNodeInput,
                                                   TemperatureNodeInput)


class NodeInputFactory:
    def __init__(self):
        pass

    def create_distance_node_input(self, distance: float,
                                   node_var_name: str, node_name: str,
                                   index: str = '0', sub_index: str = '0'):
        return DistanceNodeInput(distance,
                                 node_var_name, node_name, index, sub_index)

    def create_steering_node_input(self, steering_angle: float,
                                   node_var_name: str, node_name: str,
                                   index: str = '0', sub_index: str = '0'):
        return SteeringNodeInput(steering_angle,
                                 node_var_name, node_name, index, sub_index)

    def create_localization_node_input(self, location, node_var_name: str,
                                       node_name: str, index: str = '0',
                                       sub_index: str = '0'):
        # not sure how data will look like for location
        return LocalizationNodeInput(location, node_var_name, node_name,
                                     index, sub_index)

    def create_engine_node_input(self, set_engine: bool,
                                 node_var_name: str, node_name: str,
                                 index: str = '0', sub_index: str = '0'):
        return EngineNodeInput(set_engine,
                               node_var_name, node_name, index, sub_index)

    def create_temperature_node_input(self, temperature: float,
                                      node_var_name: str, node_name: str,
                                      index: str = '0', sub_index: str = '0'):
        return TemperatureNodeInput(temperature,
                                    node_var_name, node_name, index, sub_index)
