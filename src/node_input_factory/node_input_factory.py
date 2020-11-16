from node_input_factory.node_input_classes import (DistanceNodeInput,
                                                   SteeringNodeInput,
                                                   CoordinationNodeInput,
                                                   EngineNodeInput,
                                                   TemperatureNodeInput,
                                                   ServoNodeInput)


class NodeInputFactory:
    def __init__(self):
        pass

    def create_distance_node_input(self, distance: float,
                                   name: str, node_purpose_name: str):
        return DistanceNodeInput(distance,
                                 name, node_purpose_name)

    def create_steering_node_input(self, steering_angle: float,
                                   name: str, node_purpose_name: str):
        return SteeringNodeInput(steering_angle,
                                 name, node_purpose_name)

    def create_coordination_node_input(self, location, name: str,
                                       node_purpose_name: str):
        # not sure how data will look like for location
        return CoordinationNodeInput(location, name, node_purpose_name)

    def create_engine_node_input(self, set_engine: bool,
                                 name: str, node_purpose_name: str):
        return EngineNodeInput(set_engine,
                               name, node_purpose_name)

    def create_temperature_node_input(self, temperature: float,
                                      name: str, node_purpose_name: str):
        return TemperatureNodeInput(temperature,
                                    name, node_purpose_name)

    def create_servo_node_input(self, angle: float,
                                name: str, node_purpose_name: str):
        return ServoNodeInput(angle,
                              name, node_purpose_name)
