from abc import ABC


class Node(ABC):
    def __init__(self, value):
        # Value is eg int, float, vector, analog signal.
        self.value = value
        super().__init__()

    def read_sensor(self):
        return self.value


class DistanceNode(Node):
    # Distance as object distance
    def __init__(self, distance: float):
        self.distance = distance
        super().__init__(distance)


class SteeringNode(Node):
    def __init__(self, steering_radius: float):
        self.steering_radius = steering_radius
        super().__init__(steering_radius)


class CoordinationNode(Node):
    def __init__(self, location):
        self.location = location
        super().__init__(location)


class EngineNode(Node):
    def __init__(self, set_engine: bool):
        self.set_engine = set_engine
        super().__init__(set_engine)


class TemperatureNode(Node):
    def __init__(self, temperature: float):
        self.temperature = temperature
        super().__init__(temperature)
