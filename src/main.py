import yaml
from listener.can_open_listener import CanOpenListener
from interpreter_classes import CanOpenInterpreter
from time import sleep

if __name__ == "__main__":
    # Standard python main structure
    with open('./config.yaml', 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    can_open_interpreter = CanOpenInterpreter()
    master_node = CanOpenListener(config, can_open_interpreter)

    # main loop
    while True:
        master_node.listen_to_network()
        sleep(0.1)
