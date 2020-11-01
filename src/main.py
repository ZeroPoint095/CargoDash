import yaml
from listener.can_open_listener import CanOpenListener

if __name__ == "__main__":
    # Standard python main structure
    with open('./config.yaml', 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    masterNode = CanOpenListener(config)
