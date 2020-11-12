from struct import unpack
from node_input_factory.node_input_classes import (DistanceNodeInput,
                                                   SteeringNodeInput,
                                                   CoordinationNodeInput,
                                                   EngineNodeInput,
                                                   TemperatureNodeInput)


class NodeInputFactory:
    def __init__(self):
        pass

    def create_distance_node_input(self, distance, name, node_purpose_name):
        return DistanceNodeInput(unpack('h', distance)[0],
                                 name, node_purpose_name)

    def create_steering_node_input(self, steering_radius,
                                   name, node_purpose_name):
        return SteeringNodeInput(unpack('h', steering_radius)[0],
                                 name, node_purpose_name)

    def create_coordination_node_input(self, location, name,
                                       node_purpose_name):
        # not sure how data will look like
        return CoordinationNodeInput(location, name, node_purpose_name)

    def create_engine_node_input(self, set_engine, name, node_purpose_name):
        return EngineNodeInput(unpack('h', set_engine)[0],
                               name, node_purpose_name)

    def create_temperature_node_input(self, temperature, name,
                                      node_purpose_name):
        return TemperatureNodeInput(unpack('h', temperature)[0],
                                    name, node_purpose_name)
