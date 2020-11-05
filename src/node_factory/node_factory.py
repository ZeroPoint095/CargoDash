from node_factory.node_classes import *

class NodeFactory:
    def __init__(self):
        pass

    def create_distance_node(self, distance, name):
        return DistanceNode(distance)

    def create_steering_node(self, steering_radius, name):
        return SteeringNode(steering_radius)

    def create_coordination_node(self, location, name):
        return CoordinationNode(location)

    def create_engine_node(self, set_engine, name):
        return EngineNode(set_engine)

    def create_temperature_node(self, temperature, name):
        return TemperatureNode(temperature)