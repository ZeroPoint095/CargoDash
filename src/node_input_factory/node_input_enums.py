from enum import Enum, unique


@unique
class NodeType(Enum):
    DistanceNode = 0
    SteeringNode = 1
    CoordinationNode = 2
    EngineNode = 3
    TemperatureNode = 4
    ServoNode = 5
