class Node:
    def __init__(self):
        pass


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
