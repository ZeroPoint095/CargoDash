import yaml
import asyncio
from listener.can_open_listener import CanOpenListener
from interpreter.can_open_interpreter import CanOpenInterpreter
from vehicle_state.vehicle_classes import ConfigureableVehicle
from buffer_logger.can_buffer_logger import CanBufferLogger
from test_network.can_open_test_network import CanOpenTestNetwork


async def concurrently(master_node_loop, logger_loop):
    await asyncio.gather(master_node_loop, logger_loop)


if __name__ == "__main__":
    config_type = 'canopen_vcan'
    with open('./config.yaml', 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    if(config[config_type]['communication_protocol'] == 'canopen'):
        TestNetwork = CanOpenTestNetwork(config, config_type)

        if(TestNetwork.connected_to_network()):
            TestNetwork.test_connection()

            coach = ConfigureableVehicle(config, config_type)
            can_open_interpreter = CanOpenInterpreter(coach)
            master_node = CanOpenListener(config, config_type,
                                          can_open_interpreter)
            logger = CanBufferLogger(config, config_type)

            # Runs master-node and logger concurrently.
            if(config[config_type]['raw_can_data_logging']['enabled']):
                # Runs master-node and logger concurrently.
                asyncio.run(concurrently(master_node.async_network_loop(),
                            logger.listen_to_network()))
            else:
                asyncio.run(master_node.async_network_loop())
