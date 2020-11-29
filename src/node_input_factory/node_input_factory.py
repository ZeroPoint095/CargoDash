from node_input_factory.node_input_classes import (DistanceNodeInput,
                                                   SteeringNodeInput,
                                                   LocalizationNodeInput,
                                                   EngineNodeInput,
                                                   TemperatureNodeInput)


class NodeInputFactory:
    def __init__(self):
        pass

    def create_distance_node_input(self, distance: float,
                                   var_name: str, node_name: str):
        return DistanceNodeInput(distance,
                                 var_name, node_name)

    def create_steering_node_input(self, steering_angle: float,
                                   var_name: str, node_name: str):
        return SteeringNodeInput(steering_angle,
                                 var_name, node_name)

    def create_localization_node_input(self, location, var_name: str,
                                       node_name: str):
        # not sure how data will look like for location
        return LocalizationNodeInput(location, var_name, node_name)

    def create_engine_node_input(self, set_engine: bool,
                                 var_name: str, node_name: str):
        return EngineNodeInput(set_engine,
                               var_name, node_name)

    def create_temperature_node_input(self, temperature: float,
                                      var_name: str, node_name: str):
        return TemperatureNodeInput(temperature,
                                    var_name, node_name)
