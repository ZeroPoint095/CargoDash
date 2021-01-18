from abc import ABC, abstractmethod


class Listener(ABC):
    def __init__(self, config):
        self.config = config
        super().__init__()

    @abstractmethod
    def connect_to_network(self, channel):
        pass

    @abstractmethod
    def listen_to_network(self):
        pass

    @abstractmethod
    def inform_interpreter(self):
        pass
