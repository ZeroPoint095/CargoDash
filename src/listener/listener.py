from abc import ABC, abstractmethod


class Listener(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def listenToNetwork(self, channel):
        pass

    @abstractmethod
    def inform_interpreter(self):
        pass
    
    def log_data(self):
        pass

