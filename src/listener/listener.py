from datetime import datetime
from abc import ABC, abstractmethod


class Listener(ABC):
    def __init__(self, config):
        self.config = config
        self.directory = './logs/'
        self.log_file = datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + '.log'
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

    def log_data(self, message):
        log_file_location = self.directory + self.log_file
        with open(log_file_location, 'a') as file:
            file.write(message)
