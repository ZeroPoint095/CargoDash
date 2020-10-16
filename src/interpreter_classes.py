from abc import ABC, abstractmethod


class Interpreter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def create_coordination_node():
        pass

    @abstractmethod
    def create_steering_node():
        pass

    @abstractmethod
    def create_engine_node():
        pass

    @abstractmethod
    def create_temperature_node():
        pass


class CanOpenInterpreter(Interpreter):
    def __init__(self):
        super().__init__()
