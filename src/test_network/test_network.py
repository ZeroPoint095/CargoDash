from abc import ABC, abstractmethod


class TestNetwork(ABC):
    def __init__(self, config, config_type):
        self.config_type = config_type
        self.config = config
        super().__init__()

    @abstractmethod
    def connected_to_network():
        pass

    @abstractmethod
    def test_connection():
        pass