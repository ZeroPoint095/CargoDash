class Vehicle:
    def __init__(self, steering_wheel):
        assert isinstance(steering_wheel, SteeringWheel)
        self.steering_wheel = steering_wheel


class AutoBus(Vehicle):
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
        assert isinstance(diameter, float)
        self.diameter = diameter


class SteeringWheel:
    def __init__(self, steering_radius):
        assert isinstance(steering_radius, float)
        self.steering_radius = steering_radius


class Engine:
    def __init__(self):
        pass


class Throttle:
    def __init__(self):
        pass


Vehicle(SteeringWheel(90))
AutoBus(Engine(), SteeringWheel(90))
