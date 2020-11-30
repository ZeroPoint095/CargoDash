import canopen
import time
import struct

'''
An example of communicating with an Arduino via a canbus network using
the CanOpen protocol. This example uses a Joy-It SBC-CAN01 module connected
via SPI as a CAN interface using the GPIO pins of a Raspberry Pi.
See https://joy-it.net/en/products/SBC-CAN01 for connection and
setup instructions.

The Arduino must be running Canfestivino with .EDS and .CPP files
made in ObjDictEdit.py
#TODO add URL to arduino sketch/instructions
'''

network = canopen.Network()

master_node = canopen.LocalNode(1, 'master.eds')
slave_node = canopen.RemoteNode(5, 'slave_node_example.eds')
# .eds and object dictionary are interchangable
network.add_node(master_node)
network.add_node(slave_node)

'''
You may need to enable the CAN interface (this must be done
    after rebooting the OS)
Run the following commands in the terminal
    $ sudo ip lin set can0 up type can bitrate 500000
    $ sudo ifconfig can0 txqueuelen 10000
You can view the raw CAN messages by running
    $ candump can0
'''
network.connect(bustype='socketcan', channel='can0', bitrate=500000)


def network_scan(network):
    # This will attempt to read an SDO from nodes 1 - 127
    network.scanner.search()
    # We may need to wait a short while here to allow all nodes to respond
    time.sleep(0.5)
    for node_id in network.scanner.nodes:
        print("Found node %d!" % node_id)
        print("Hex:", node_id)


def read_without_od(node, index, subindex):
    '''reads from the node without using the Object Dictionary,
       returns hex byte string
    '''
    readValue = node.sdo.upload(index, subindex)
    readValue = struct.unpack('h', readValue)
    print(readValue[0])
    return readValue[0]


def write_without_od(node, index, subindex, value):
    '''writes to the node without using the Object Dictionary'''
    data = struct.pack('h', value)
    node.sdo.download(index, subindex, data)


def read_with_od(node, manufacturerObject_name: str):
    '''
    reads to the node using the Object Dictionary, assumes
    there is no subindex.
    to read subvalue, use:
        node.sdo['ManufacturerObjectName']['ManufacturerSubObjectName'].raw
    raw converts value automatically. .phys, .desc & .bits are also possible.
    '''
    readValue = node.sdo[manufacturerObject_name].raw
    return readValue


def write_with_od(node, manufacturerObject_name: str, value):
    '''
    writes to the node using the Object Dictionary, assumes
    there is no subindex.
    to write to subvalue, use:
        node.sdo['ManufacturerObjectName']['ManufacturerSubObjectName'].write(value)
    '''
    node.sdo[manufacturerObject_name].write(value)


while(True):
    '''
    reads sensor data and writes the read value to the actuator
    '''
    # without using object dictionary
    #     data = read_without_od(slave_node, 0x2000, 0)
    #     write_without_od(slave_node, 0x2001, 0, data)

    # using object dictionary
    data = read_with_od(slave_node, 'Sensor')
    write_with_od(slave_node, 'Actuator', data)

    time.sleep(0.1)

network.disconnect()
