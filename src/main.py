import yaml
from listener.can_open_listener import CanOpenListener
from interpreter.can_open_interpreter import CanOpenInterpreter
from vehicle_state.vehicle_classes import ConfigureableVehicle
from time import sleep

if __name__ == "__main__":
    config_type = 'canopen_vcan'
    with open('./config.yaml', 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    coach = ConfigureableVehicle(config, config_type)
    can_open_interpreter = CanOpenInterpreter(coach)
    master_node = CanOpenListener(config, config_type, can_open_interpreter)

    # main loop
    while True:
        master_node.listen_to_network()
        sleep(0.1)
