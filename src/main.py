import yaml
from listener.can_open_listener import CanOpenListener
from time import sleep

if __name__ == "__main__":
    # Standard python main structure
    with open('./config.yaml', 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    can_open_interpreter = 
    master_node = CanOpenListener(config)

    # main loop
    while True:
        sleep(0.1)
        master_node.listen_to_network()
