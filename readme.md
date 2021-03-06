﻿# CargoDash Usage Guide
This document will help you to understand how to make use of CargoDash. CargoDash is a diagnostics tool for developing autonomous vehicles and is written in Python code (version 3.8.5). For any questions please feel free to create an issue.

## External Python Dependencies
```
    aiohttp v3.7.3
    asyncio v3.4.3
    can v3.3.4
    canopen v1.1.0
    numpy v1.19.4
    pyyaml v5.3.1
```
## Installation
1. Clone the repository
```
    git clone https://github.com/ZeroPoint095/CargoDash
```
2. Install the Python dependencies with pip3
```
    pip3 install -r requirements.txt
```
&nbsp;&nbsp;&nbsp;3a. For a *virtual* CANbus use the following command to initialise the CANbus:
```
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

&nbsp;&nbsp;&nbsp;3b. For a *real* CANbus use the following command:
```
sudo ip link set can0 up type can bitrate 500000
sudo ifconfig can0 txqueuelen 20000
```
&nbsp;&nbsp;&nbsp;First time setting a *real* CANbus? See this [document](https://github.com/ZeroPoint095/CANFestivino/blob/master/INSTALLATION-GUIDE.md) first!

4. To run the CargoDash API manually you need to run the following in 3 separate terminals:

Terminal 1:
```
    python3 src/main.py
```
Terminal 2:
```
    python3 src/http_server/cargo_dash_http_server.py
```  
Terminal 3:
```
    cd src/frontend
    python3 -m http.server
```  



## Introduction
CargoDash is a tool that listens to incoming messages and sets the values of these messages into user-defined nodes. These user-defined nodes can be requested with CargoDash's HTTP-server. The tool can also be used to update these user-defined nodes with new values. Besides this, it logs all raw incoming messages into a buffered logger. 

For now, CargoDash works only with CanOpen messages but with the architecture of CargoDash, you should be able to add your desired message protocol.

The buffered logger can be requested to log all messages from the buffer on command. The buffer is circular and records the messages continuously. When the buffer is full then it continues by overwriting the oldest messages.  For example, when the buffer just filled in index 1024 and it has a range from index 0 to index 1024 then it starts over again from index 0. The buffer gets filled from 0 to 1024 again. The logger has many useful purposes. You can request the buffer on a dangerous event or just when a user wants to see the log.

## Our usage
We created CargoDash to listen to a CanOpen network and use it for the Smarterdam project. The Smarterdam project is funded by Rotterdam University of Applied Sciences. CargoDash is able to track all incoming CanOpen messages and we are able to give more meaning to messages that have been send and received.

In our application, we created a network of Arduino's that communicate with a Raspberry Pi running the CargoDash code. For the communication between the Arduino's and the Raspberry Pi, we set up a can bus network in which all micro-controllers communicate using the CanOpen protocol. For the Arduino's to communicate with CanOpen, we forked [jgeisler0303's](https://github.com/jgeisler0303/CANFestivino) repository, fixed some bugs and adapted it more to our use case. Our repository can be found [here](https://github.com/ZeroPoint095/CANFestivino).

## Using the configuration file for CanOpen (config.yaml)

Inside the code block below you can read a detailed description of which configurations that CargoDash uses. In general, we prefer that CargoDash can be configured from one file such as the config.yaml file instead of multiple configuration places. This makes CargoDash more user-friendly and centralized. 
```yaml
    # selected_config is the variable that sets which configuration is 
    # selected for CargoDash. So for this instance, it makes use of configuration
    # canopen_vcan.
    selected_config: canopen_vcan
    
    # canopen_vcan is a configuration example for the CanOpen protocol.
    # With a similar pattern you can create multiple canopen configurations.
    # For now we use canopen_vcan as example. All these paramters inside canopen_vcan 
    # are used for CargoDash's CanOpen implementation.
    canopen_vcan:
        
        # Sets the bustype of the CanOpen network. 
        bustype: socketcan 
        
        # Sets the channel name of the CanOpen network
        channel: vcan0 
        
        # Sets the bitrate of CanOpen the network
        bitrate: 500000 
        
        # Sets the nodes which exist inside the network.
        # This is done in an array with object that contain information needed for CargoDash.
        # Every object needs to contain these attributes
        #       local : sets if the node is either remote or local
        #       eds_location : path to the eds file of the node
        #       node_purpose : object containing name and type of node:
        #                      name: Short description of the node
        #                      type: integer that should reflect the types of the nodes 
        #                            at node_input_factory/node_input_enums.
        #       For example the node_purpose type below is 0 and that is reflected with a
        #       DistanceNode.

        nodes: [{local: false, eds_location: 'eds_files/Arduino1.eds', node_purpose: {name: 'Front view object distance', type: 0}}]
        
        # Sets the max speed of wheelNodes.
        max_speed_in_ms: 3 
        
        # Object related to can data logging.
        # Our logger makes use of a buffered logger implementation.

        raw_can_data_logging: {
            # Enables of Disables the buffered logger.
            enabled: true,

            # The size of the buffer so with it can contain 1024 can messages.
            buffer: 1024,
            
            # At every n-th message update shared memory
            shm_update_interval_threshold: 100
        }
```
## Extending CargoDash Communication Possibilities

For now, CargoDash is only able to work with the CanOpen protocol but it has the potential to work with more communication protocols. If you want to add a communication protocol then you should add a new interpreter and a new listener. You can easily create a new listener class that uses the same methods and interfaces as the abstract listener class. The same goes for the interpreter. The public methods needs to use the same arguments as it's abstract class. It's important that you create nodes from the NodeFactory inside your interpreter. The NodeFactory class creates 'Node Input' objects which can be used to change the vehicle's state. In the diagram below you can have an understanding of CargoDash internal class interaction works.


![CargoDash Architecture](img/api_cargodash_v9.png "CargoDash Architecture")

## Adding Nodes
In CargoDash we already implemented certain standard nodes that would exist in a real vehicle such as SteeringNode, TemperatureNode, and more. But if you want to add your own, custom node you can add it by changing some files. You can do this using the changes described below using a LidarNode as an example.

Just add an enum to the enums list.
```python
    # Add to: node_input_factory/node_input_enums.py

    ...
    LidarNode=5
```

At the end of the file add the new class *LidarNodeInput*.
```python
    # Add to: node_input_factory/node_input_classes.py

    ...
    class LidarNodeInput(NodeInput):
    # Enum 5
    def __init__(self, distance: float, name: str, node_name: str,
                 **additional_attributes):
        super().__init__(distance, name, node_name)

```

Inside the class *NodeInputFactory* add a new method.
```python
    # Add to: node_input_factory/node_input_factory.py

    ...
    def create_lidar_node_input(self, distance: float,
                                name: str, node_name: str, 
                                **additional_attributes):
        return LidarNodeInput(distance,
                              name, node_name)
```
And don't forget to import *LidarNodeInput* at the *node_input_factory.py* file.

In class *CanOpenInterpreter* you need to add the node check between the last elif and else.
You should make it similar like this. It is really depending on which extra attributes you want to give as well.
The obligatory attributes are the new value, the name of the variable and the name of node. 
```python
    # Change in: interpreter/can_open_interpreter.py

    ...
    elif(NodeType.LidarNode == node_type):
        n_input = self.node_input_factory.create_lidar_node_input(
            unpack(unpack_format, node_data['sdo_value'])[0],
            node_data['sdo_name'], node_data['node_name'],
            index=node_data['index'],
            sub_index=node_data['sub_index'],
            data_type=node_data['sdo_data_type'],
            access_type=node_data['access_type'],
            parent_name=node_data['parent_name'])
    ...
```

In the constructor of class *ConfigureableVehicle* inside the file *vehicle_classes.py*, you should add a new property like:
```python
    # Add to: vehicle_state/vehicle_classes.py

    self.lidar_nodes = array([])
```
So that all the lidar nodes can be kept in array so we can request for them whenever we need it.

At the end of the file you should add:
```python
    # Add to: vehicle_state/vehicle_classes.py

    ...
    class LidarSensor(Node):
        def __init__(self, name):
            self.distance = 0
            super().__init__(name)

```

Then in private method *_add_node_to_vehicle* add:
```python
    # Add to: vehicle_state/vehicle_classes.py

    ...
    elif(node_type == NodeType.LidarNode):
        if(not self._is_node_existing(self.lidar_nodes,
                                        node_name)):
            new_node = LidarSensor(node_name)
            self.distance_nodes = append(
                self.distance_nodes, new_node)
    ...
```
Lastly you should add in method *edit_vehicle_state*:
```python
    # Add to: vehicle_state/vehicle_classes.py
    
    ...
    elif(input_type == LidarNodeInput):
        node = self._get_node(self.lidar_nodes, node_input)
        if(node is not None):
            node.update_variable_list(node_input.node_var_name,
                                      node_input.__dict__)
    ...
```

The private method update_variable_list is the standard way to put new values into the nodes. 
But inside the class LidarSensor you could create your own custom method that updates the values.

According to your own business logic. 

# CargoDash API Usage

### Retrieve all nodes
```http
    GET /allnodes
```
Returns array with all nodes in json format.

Eg. returns
```javascript
    [{
        type : 'DistanceNode',
        node_name : 'Front view object distance',
        variables : [
            ...
        ]
    },
    {
        type : 'SteeringNode',
        node_name : 'Steering wheel',
        variables : [
            ...
        ]
    }],
    ...
```
***
### Retrieve specified node
```http
    GET /node/:id
```
Returns desired node information based on node ID.

#### Parameters
id :    id of a node expects integer between 1-127 (not hex value).

Eg. returns
```javascript
    {
        type : 'DistanceNode',
        node_name : 'Front view object distance',
        variables : [
            ...
        ]
    }
```
***
### Retrieve specified variable
```http
    GET /node/:id/:var_name
```
Returns desired variable in json format.
#### Parameters

id : id of a specified node expects integer between 1-127 (not hex value).

var_name: name of the desired variable.

Eg. returns
```javascript
{
    name: 'variable',
    index: '0x2000',
    sub_index: '0',
    value : '900'
}
```

***
### Update specified variable
```http
    POST /node/:id/:var_name
```
Receives a post request that wants to update a value of a variable.
Returns a message that says value is changed succesfully.
#### Parameters:
id : id of a specified node expects integer between 1-127 (not hex value).

var_name: name of the variable that needs to be changed.

Request body:
```javascript
{
    value: 'new_value'
}
```

Note: This post request has lower importance for us. Hopefully we are able to implement this.
***
### Retrieve logging
```http
    GET /getloggingbuffer
```
Returns the current logging buffer (raw messages) in json format.

Eg. returns
```javascript
[
    {
        timestamp: '21314313',
        ID: '123',
        Data: 'FF 88 HA 99 12 77 88 99',
        Channel: 'vcan0'
    },
    {
        ...
    }
]
```
