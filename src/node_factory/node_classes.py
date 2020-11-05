from abc import ABC


class Node(ABC):
    def __init__(self, value, name):
        # Value is eg int, float, vector, analog signal.
        self.name = name
        self.value = value
        super().__init__()

    def read_node(self):
        return self.value

    def write_node(self, new_value):
        self.value = new_value


class DistanceNode(Node):
    # Distance as object distance
    def __init__(self, distance: float, name: str):
        super().__init__(distance, name)


class SteeringNode(Node):
    def __init__(self, steering_radius: float, name: str):
        super().__init__(steering_radius, name)


class CoordinationNode(Node):
    def __init__(self, location, name: str):
        super().__init__(location, name)


class EngineNode(Node):
    def __init__(self, set_engine: bool, name: str):
        super().__init__(set_engine, name)


class TemperatureNode(Node):
    def __init__(self, temperature: float, name: str):
        super().__init__(temperature, name)
