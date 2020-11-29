from abc import ABC


class NodeInput(ABC):
    def __init__(self, value, var_name, node_name):
        ''' NodeInput Object used to change to state of the vehicle.

            value : any
                Node value to change the state of the vehicle.

            name : string
                Name belonging to a variable within the node.

            node_name : string
                Description what the node is functioning for.

        '''
        self.var_name = var_name
        self.value = value
        self.node_name = node_name
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
    def __init__(self, distance: float, var_name: str, node_name: str):
        super().__init__(distance, var_name, node_name)


class SteeringNodeInput(NodeInput):
    # Enum 1
    def __init__(self, steering_angle: float, var_name: str, node_name: str):
        super().__init__(steering_angle, var_name, node_name)


class LocalizationNodeInput(NodeInput):
    # Enum 2
    def __init__(self, location: str, var_name: str, node_name: str):
        super().__init__(location, var_name, node_name)


class EngineNodeInput(NodeInput):
    # Enum 3
    def __init__(self, set_engine: bool, var_name: str, node_name: str):
        super().__init__(set_engine, var_name, node_name)


class TemperatureNodeInput(NodeInput):
    # Enum 4
    def __init__(self, temperature: float, var_name: str, node_name: str):
        super().__init__(temperature, var_name, node_name)
