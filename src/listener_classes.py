from abc import ABC, abstractmethod


class Listener(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def listenToChannel():
        pass

    @abstractmethod
    def log_data():
        pass

    @abstractmethod
    def inform_interpreter():
        pass


class CanOpenListener(Listener):
    def __init__(self):
        super().__init__()