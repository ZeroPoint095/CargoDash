from abc import ABC


class NodeInput(ABC):
    def __init__(self, value, name, node_purpose):
        ''' NodeInput Object used to change to state of the vehicle.

            value : any
                Node value to change the state of the vehicle.

            name : string
                Name given with the value.

            node_purpose : string
                Description what the node is functioning for.

        '''
        self.name = name
        self.value = value
        self.node_purpose = node_purpose
        super().__init__()

    def read_node_input(self):
        ''' Returns the value of the node input object.
        '''
        return self.value

    def write_node_input(self, new_value):
        ''' Changes the value of the node input object.

            new_value : void
                The new value for the node input object.

            Returns void.
        '''
        self.value = new_value


class DistanceNodeInput(NodeInput):
    # Enum 0
    # Distance as object distance
    def __init__(self, distance: float, name: str, node_purpose: str):
        super().__init__(distance, name, node_purpose)


class SteeringNodeInput(NodeInput):
    # Enum 1
    def __init__(self, steering_angle: float, name: str, node_purpose: str):
        super().__init__(steering_angle, name, node_purpose)


class CoordinationNodeInput(NodeInput):
    # Enum 2
    def __init__(self, location: str, name: str, node_purpose: str):
        super().__init__(location, name, node_purpose)


class EngineNodeInput(NodeInput):
    # Enum 3
    def __init__(self, set_engine: bool, name: str, node_purpose: str):
        super().__init__(set_engine, name, node_purpose)


class TemperatureNodeInput(NodeInput):
    # Enum 4
    def __init__(self, temperature: float, name: str, node_purpose: str):
        super().__init__(temperature, name, node_purpose)


class ServoNodeInput(NodeInput):
    # Enum 5
    def __init__(self, angle: float, name: str, node_purpose: str):
        super().__init__(angle, name, node_purpose)
