from enum import Enum
from abc import ABC
from numpy import array, append
from node_input_factory.node_input_enums import NodeType
from node_input_factory.node_input_classes import (DistanceNodeInput,
                                                   SteeringNodeInput,
                                                   LocalizationNodeInput,
                                                   EngineNodeInput,
                                                   TemperatureNodeInput)


class WheelPosition(Enum):
    front_left = 0
    front_right = 1
    rear_left = 2
    rear_right = 3


class Node(ABC):
    def __init__(self, purpose):
        # Purpose of the node itself.
        self.id = None
        self.purpose = purpose
        # Variables that the node uses.
        # Variable includes name and value.
        self.variables = array([])

    def update_variable_list(self, name, value):
        updated = False
        for variable in self.variables:
            if(variable['name'] == name):
                updated = True
                variable['value'] = value
        if(not updated):
            self.variables = append(
                self.variables, {'name': name, 'value': value})


class Steering(Node):
    def __init__(self, purpose):
        self.current_steering_angle = 0
        super().__init__(purpose)

    def change_angle(self, steering_angle: float):
        # Changes the current steering angle.
        self.current_steering_angle = steering_angle


class Engine(Node):
    def __init__(self, purpose):
        self.engine_running = False
        super().__init__(purpose)

    def turn_on_off(self, on):
        if(on):
            # Turns engine on.
            self.engine_running = True
        else:
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
        where it should listen to. The nodes are configured
        in the config.yaml file.
    '''
    def __init__(self, config, config_type):
        ''' config : yaml_file_stream
                The configured yaml file that contains details for the
                connection type.

            config_type: string
                The selected configuration that is going to be used.
                The configurations are defined in 'config.yaml'.
        '''
        self.config = config
        self.distance_nodes = array([])
        self.temperature_nodes = array([])
        self.engine_nodes = array([])
        nodes = config[config_type]['nodes']
        # Firstly, initializes vehicle according nodes that
        # are listed in the configuration file.
        for i in range(len(nodes)):
            self._add_node_to_vehicle(nodes[i]['node_purpose'])
        Vehicle.__init__(self)

    def edit_vehicle_state(self, node_input):
        ''' Changes the vehicle state with a incoming
            node input.

            node_input : any NodeInput
                The node input that came from the interpreter. That gives
                the changes as an input for the vehicle state.

        '''
        input_type = type(node_input)

        if(input_type == DistanceNodeInput):
            node = self._get_node(self.distance_nodes, node_input)
            if(node is not None):
                node.set_distance(node_input.value)
        elif(input_type == SteeringNodeInput):
            if(self.steering is not None):
                self.steering.change_angle(node_input.value)
        elif(input_type == LocalizationNodeInput):
            # TODO: add LocalizationNode for now less relevant
            pass
        elif(input_type == EngineNodeInput):
            node = self._get_node(self.engine_nodes, node_input)
            if(node is not None):
                node.turn_on_off(node_input.value)
        elif(input_type == TemperatureNodeInput):
            # TODO: add TemperatureNode for now less relevant
            pass

    def _add_node_to_vehicle(self, node_purpose):
        # Automatically add nodes that are defined in the
        # config.yaml file.
        node_type = NodeType(node_purpose['type'])
        node_name = node_purpose['name']

        # ID used for HTTPSERVER this is not similar as
        # the node ids for the canbus network.
        http_index = 0

        if(node_type == NodeType.DistanceNode):
            if(not self._is_node_existing(self.distance_nodes,
                                          node_name)):
                new_node = DistanceSensor(node_name)
                new_node.id = http_index
                self.distance_nodes = append(
                    self.distance_nodes, new_node)
        elif(node_type == NodeType.SteeringNode):
            # We don't keep a list for steering because we don't
            # expect multiple steering nodes in general.
            if(self.steering is None):
                self.steering = Steering(node_name)
                self.steering.id = http_index
        elif(node_type == NodeType.LocalizationNode):
            # TODO: add LocalizationNode for now less relevant
            pass
        elif(node_type == NodeType.EngineNode):
            if(not self._is_node_existing(self.engine_nodes,
                                          node_name)):
                new_node = Engine(node_name)
                new_node.id = http_index
                self.engine_nodes = append(
                    self.engine_nodes, new_node)
        elif(node_type == NodeType.TemperatureNode):
            # TODO: add TemperatureNode for now less relevant
            pass
        http_index = http_index + 1

    def _get_node(self, node_list, node_input):
        for node in node_list:
            if(node.purpose == node_input.node_purpose):
                return node
        return None

    def _is_node_existing(self, node_list, purpose):
        existing = False
        for node in node_list:
            if(node.purpose == purpose):
                existing = True
        return existing


class Wheel(Node):
    def __init__(self, wheel_diameter: float, wheel_position: int,
                 suspension_stiffness: float, tire_pressure: float,
                 max_speed_in_ms=3):
        self.tire = Tire(wheel_diameter, tire_pressure)
        self.suspension = Suspension(suspension_stiffness)
        self.wheel_position = wheel_position
        self.speed = 0
        self.max_speed_in_ms = 3

    def get_speed(self):
        return self.speed

    def set_speed(self, new_speed: float):
        if new_speed <= self.max_speed_in_ms:
            self.speed = new_speed
        else:
            print(new_speed, " exceeds max speed of ",
                  self.max_speed_in_ms, ". \n Speed set to ", 
                  self.max_speed_in_ms)
            self.speed = self.max_speed_in_ms


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

    def set_distance(self, distance):
        self.distance = distance
