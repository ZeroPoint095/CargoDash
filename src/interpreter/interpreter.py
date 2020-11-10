from abc import ABC, abstractmethod


class Interpreter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def inform_interpreter(object):
        pass
