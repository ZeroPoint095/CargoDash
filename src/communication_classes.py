''' Not sure if we are able to use this but we can leave it for now  '''

from abc import ABC


class CommunicationProtocol(ABC):
    def __init__(self):
        pass


class CanBus(CommunicationProtocol):
    def __init__(self):
        CommunicationProtocol.__init__(self)
