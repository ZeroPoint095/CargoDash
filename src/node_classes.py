class Node:
    def __init__(self, node_type, value_type):
        # Node type is eg speed, force, distance, temperature, etc.
        # Value type is eg int, float, vector, analog signal.
        self.node_type = node_type
        self.value_type = value_type

    def read_sensor():
        return sensor_value


class DistanceNode(Node):
    def __init__(self, distance):
        self.distance = distance
        Node.__init__(self)


class SteeringNode(Node):
    def __init__(self, steering_radius):
        self.steering_radius = steering_radius
        Node.__init__(self)


class CoordinationNode(Node):
    def __init__(self):
        Node.__init__(self)
