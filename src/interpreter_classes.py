from abc import ABC, abstractmethod


class Interpreter(ABC):
    def __init__(self):
        super().__init__()

    #@abstractmethod
    def create_coordination_node():
        pass

    #@abstractmethod
    def create_steering_node():
        pass

    #@abstractmethod
    def create_engine_node():
        pass

    #@abstractmethod
    def create_temperature_node():
        pass

    @abstractmethod
    def inform_interpreter(object):
        pass


class CanOpenInterpreter(Interpreter):
    def __init__(self):
        super().__init__()

    def inform_interpreter(self, sdo_object):
        # Work in progress
        print(sdo_object)
