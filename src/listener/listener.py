from abc import ABC, abstractmethod


class Listener(ABC):
    def __init__(self, config):
        self.config = config
        super().__init__()

    @abstractmethod
    def connect_to_network(self):
        pass

    @abstractmethod
    def listen_to_network(self, nodes):
        pass

    @abstractmethod
    def async_network_loop(self):
        pass

    @abstractmethod
    def inform_interpreter(self, node_data):
        pass

    @abstractmethod
    def set_interpreter(self, interpreter):
        pass
