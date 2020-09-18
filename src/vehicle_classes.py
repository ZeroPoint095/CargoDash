MAX_SPEED = 3


class Vehicle:
    def __init__(self, steering_wheel):
        assert isinstance(steering_wheel, SteeringWheel)
        self.steering_wheel = steering_wheel


class Coach(Vehicle):
    def __init__(self, engine, steering_wheel):
        assert isinstance(engine, Engine)
        self.engine = engine
        self.fl_wheel = Wheel(27)
        self.fr_wheel = Wheel(27)
        self.rl_wheel = Wheel(27)
        self.rr_wheel = Wheel(27)
        Vehicle.__init__(self, steering_wheel)


class Tire:
    def __init__(self):
        pass


class Wheel:
    def __init__(self, diameter):
        self.diameter = diameter
        self.speed = 0

    def get_speed(self):
        return read_speed_sensor()

    def set_speed(self, new_speed):
        if new_speed <= MAX_SPEED:
            self.speed = new_speed
        else:
            print(new_speed, " exceeds max speed of ", MAX_SPEED, ". \n Speed set to ", MAX_SPEED)
            self.speed = MAX_SPEED


class SteeringWheel:
    def __init__(self, steering_radius):
        self.steering_radius = steering_radius


class Engine:
    def __init__(self):
        pass


class Throttle:
    def __init__(self):
        pass


class Brake:
    def __init__(self):
        # Inherent from wheel?
        pass

    def brake(self, force_percent):
        # Brake with a certain amount of force, eg 10% for gradual
        # decrease in speed, 90% for emergency stop
        # (probably blocking the wheels).
        pass


class EmergencyStop:
    def __init__(self):
        pass


class Sensor:
    def __init__(self, sensor_type, value_type):
        # Sensor type is eg speed, force, distance, temperature, etc.
        # Value type is eg int, float, vector, analog signal.
        self.sensor_type = sensor_type
        self.value_type = value_type

    def read_sensor():
        sensor_value = None
        return sensor_value


Vehicle(SteeringWheel(90))
Coach(Engine(), SteeringWheel(90))
