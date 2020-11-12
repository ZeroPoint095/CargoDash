from enum import Enum
from abc import ABC
from node_input_factory.node_input_enums import NodeType
from node_input_factory.node_input_classes import (DistanceNodeInput,
                                                   SteeringNodeInput,
                                                   CoordinationNodeInput,
                                                   EngineNodeInput,
                                                   TemperatureNodeInput)

MAX_SPEED = 3


class WheelPosition(Enum):
    front_left = 0
    front_right = 1
    rear_left = 2
    rear_right = 3


class Node(ABC):
    def __init__(self, purpose):
        # Purpose of the node itself.
        self.purpose = purpose
        # Variables that the node uses.
        # Variable includes name and value.
        self.variables = []

    def update_variable_list(self, name, value):
        updated = False
        for variable in self.variables:
            if(variable['name'] == name):
                updated = True
                variable['value'] = value
        if(not updated):
            self.variables.append({'name': name, 'value': value})


class Steering(Node):
    def __init__(self):
        self.current_steering_radius = 0

    def change_radius(self, steering_radius: float):
        # Changes the current steering radius.
        self.current_steering_radius = steering_radius


class Engine(Node):
    def __init__(self):
        self.engine_running = False

    def turn_on(self):
        # Turns engine on.
        self.engine_running = True

    def turn_off(self):
        # Turns engine off.
        self.engine_running = False


class Vehicle(ABC):
    def __init__(self):
        super().__init__()

    def get_speed(self):
        average_speed = 0
        for wheel in self.wheels:
            average_speed += wheel.speed
        return float(average_speed / len(self.wheels))


class ConfigureableVehicle(Vehicle):
    ''' This vehicle is completely dependent on the nodes
        where it should listen to.
    '''
    def __init__(self, config, config_type):
        self.distance_nodes = []
        self.coordination_nodes = []
        self.temperature_nodes = []
        self.engine_nodes = []
        nodes = config[config_type]['nodes']
        for i in range(len(nodes)):
            self._add_node_to_vehicle(nodes[i]['node_purpose'])
        Vehicle.__init__(self)
    
    def _add_node_to_vehicle(self, node_purpose):
        node_type = NodeType(node_purpose['type'])
        if(node_type == NodeType.DistanceNode):
            if(len(self.distance_nodes) == 0):
                new_node = DistanceSensor(node_purpose['name'])
                self.distance_nodes.append(new_node)
            else:
                pass
        elif(node_type == NodeType.SteeringNode):
            if(self.steering is None):
                pass
            else:
                print('?? 2 steering nodes ??')
        elif(node_type == NodeType.CoordinationNode):
            if(len(self.coordination_nodes) == 0):
                pass
            else:
                pass
        elif(node_type == NodeType.EngineNode):
            if(len(self.engine_nodes) == 0):
                pass
            else:
                pass
        elif(node_type == NodeType.TemperatureNode):
            if(len(self.temperature_nodes) == 0):
                pass
            else:
                pass

    def edit_vehicle_state(self, node_input):
        input_type = type(node_input)
        if(input_type == DistanceNodeInput):
            node = self._get_node(self.distance_nodes, node_input)
            if(node is not None):
                node.distance = node_input.value
        elif(input_type == SteeringNodeInput):
            print('steering input incoming')
        elif(input_type == CoordinationNodeInput):
            node = self._get_node(self.coordination_nodes, node_input)
            if(node is not None):
                pass
        elif(input_type == EngineNodeInput):
            node = self._get_node(self.engine_nodes, node_input)
            if(node is not None):
                pass
        elif(input_type == TemperatureNodeInput):
            node = self._get_node(self.temperature_nodes, node_input)
            if(node is not None):
                pass

    def _get_node(self, node_list, node_input):
        for node in node_list:
            if(node.purpose == node_input.node_purpose):
                return node
        return None


class Wheel(Node):
    def __init__(self, wheel_diameter: float, wheel_position: int,
                 suspension_stiffness: float, tire_pressure: float):
        self.tire = Tire(wheel_diameter, tire_pressure)
        self.suspension = Suspension(suspension_stiffness)
        self.wheel_position = wheel_position
        self.speed = 0

    def get_speed(self):
        return self.speed

    def set_speed(self, new_speed: float):
        if new_speed <= MAX_SPEED:
            self.speed = new_speed
        else:
            print(new_speed, " exceeds max speed of ",
                  MAX_SPEED, ". \n Speed set to ", MAX_SPEED)
            self.speed = MAX_SPEED


class Tire:
    def __init__(self, wheel_diameter: float, tire_pressure: float):
        self.wheel_diameter = wheel_diameter
        self.tire_pressure = tire_pressure


class Suspension(Node):
    def __init__(self, stiffness: float):
        self.stiffness = stiffness


class Throttle(Node):
    def __init__(self):
        pass

    def throttle_activated(self, force_percent: float):
        # Throttles with a certain amount of force.
        pass


class Brake(Node):
    def __init__(self):
        # Inherent from wheel?
        pass

    def brake_activated(self, force_percent: float):
        # Brake with a certain amount of force, eg 10% for gradual
        # decrease in speed, 90% for emergency stop
        # (probably blocking the wheels).
        pass


class EmergencyStop(Node):
    def __init__(self):
        pass

    def stop_activated(self):
        # Stop movement/steering
        pass


class DistanceSensor(Node):
    def __init__(self, purpose):
        self.distance = 0
        super().__init__(purpose)

    def set_distance(self, distance: float):
        self.distance = distance
