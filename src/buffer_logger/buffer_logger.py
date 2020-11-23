from abc import ABC, abstractmethod


class BufferLogger(ABC):
    def __init__(self, config, config_type):
        self.config = config
        self.config_type = config_type
        self.directory = './logs/'
        super().__init__()

    @abstractmethod
    def listen_to_network(self):
        pass

    @abstractmethod
    def release_memorized_messages(self):
        pass
