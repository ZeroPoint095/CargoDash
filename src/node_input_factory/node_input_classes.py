from abc import ABC


class NodeInput(ABC):
    def __init__(self, value, name, node_purpose):
        # Value is eg int, float, vector, analog signal.
        self.name = name
        self.value = value
        self.node_purpose = node_purpose
        super().__init__()

    def read_node_input(self):
        return self.value

    def write_node_input(self, new_value):
        self.value = new_value


class DistanceNodeInput(NodeInput):
    # Enum 0
    # Distance as object distance
    def __init__(self, distance: float, name: str, node_purpose: str):
        super().__init__(distance, name, node_purpose)
        print(self.value)


class SteeringNodeInput(NodeInput):
    # Enum 1
    def __init__(self, steering_radius: float, name: str, node_purpose: str):
        super().__init__(steering_radius, name, node_purpose)


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
