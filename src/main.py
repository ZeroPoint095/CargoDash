import yaml
from listener.can_open_listener import CanOpenListener
from interpreter.can_open_interpreter import CanOpenInterpreter
from vehicle_state.vehicle_classes import Coach
from time import sleep

if __name__ == "__main__":
    # Standard python main structure
    with open('./config.yaml', 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    coach = Coach(config)
    can_open_interpreter = CanOpenInterpreter(coach)
    master_node = CanOpenListener(config, 'canopen_vcan', can_open_interpreter)

    # main loop
    while True:
        master_node.listen_to_network()
        sleep(0.1)
