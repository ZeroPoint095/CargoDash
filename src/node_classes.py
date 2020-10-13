class Node:
    def __init__(self, node_type, value_type):
        # Node type is eg speed, force, distance, temperature, etc.
        # Value type is eg int, float, vector, analog signal.
        self.node_type = node_type
        self.value_type = value_type

    def read_sensor():
        pass


class DistanceNode(Node):
    # Distance as object distance
    def __init__(self, distance):
        self.distance = distance
        Node.__init__(self)


class SteeringNode(Node):
    def __init__(self, steering_radius):
        self.steering_radius = steering_radius
        Node.__init__(self)


class CoordinationNode(Node):
    def __init__(self, location):
        self.location = location
        Node.__init__(self)


class EngineNode(Node):
    def __init__(self, set_engine):
        self.set_engine = set_engine
        Node.__init__(self)


class TemperatureNode(Node):
    def __init__(self, temperature):
        self.temperature = temperature
        Node.__init__(self)
