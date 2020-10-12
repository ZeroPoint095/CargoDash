from enum import Enum
from abc import ABC

MAX_SPEED = 3


class WheelPosition(Enum):
    front_left = 0
    front_right = 1
    rear_left = 2
    rear_right = 3


class SteeringWheel:
    def __init__(self, steering_radius: float):
        self.current_steering_radius = steering_radius

    def change_radius(self, steering_radius: float):
        # Changes the current steering radius.
        self.current_steering_radius = steering_radius


class Engine:
    def __init__(self):
        self.engine_running = False

    def turn_on(self):
        # Turns engine on.
        self.engine_running = True

    def turn_off(self):
        # Turns engine off.
        self.engine_running = False


class Vehicle(ABC):
    def __init__(self, steering_wheel: SteeringWheel):
        self.steering_wheel = steering_wheel
        super().__init__()

    def get_speed(self):
        average_speed = 0
        for wheel in self.wheels:
            average_speed += wheel.speed
        return average_speed / len(self.wheels)


class Coach(Vehicle):
    def __init__(self, engine: Engine, steering_wheel: SteeringWheel):
        self.engine = engine
        self.wheels = [Wheel(27, wheel_position, 100, 2.1)
                       for wheel_position in range(4)]
        self.throttle = Throttle()
        self.brake = Brake()
        self.emergency_stop = EmergencyStop()
        Vehicle.__init__(self, steering_wheel)


class Wheel:
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


class Suspension:
    def __init__(self, stiffness: float):
        self.stiffness = stiffness


class Throttle:
    def __init__(self):
        pass

    def throttle_activated(self, force_percent: float):
        # Throttles with a certain amount of force.
        pass


class Brake:
    def __init__(self):
        # Inherent from wheel?
        pass

    def brake_activated(self, force_percent: float):
        # Brake with a certain amount of force, eg 10% for gradual
        # decrease in speed, 90% for emergency stop
        # (probably blocking the wheels).
        pass


class EmergencyStop:
    def __init__(self):
        pass

    def stop_activated(self):
        # Stop movement/steering
        pass


Vehicle(SteeringWheel(90))
Coach(Engine(), SteeringWheel(90))
