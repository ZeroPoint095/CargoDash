import json
import ast
import canopen
import logging
import yaml
import numpy as np
import zlib as zl
from aiohttp import web
from multiprocessing import shared_memory

routes = web.RouteTableDef()
INTERFACE = 'canopen_vcan'
all_saved_nodes = np.array([])


def set_headers(response):
    ''' Updates the HTTP headers
        so that we are able to bypass CORS errors.

        Returns the updated Response.
    '''
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


def uncompress_logging_information():
    ''' Uncompresses the shared logging information.

        Returns the logs as string.
    '''
    try:
        shared_logs = shared_memory.ShareableList(name='shm_buff_data')
    except FileNotFoundError:
        return {'message': 'Cannot fetch buffered logger'}
    all_logs = zl.decompress(shared_logs[0]).decode('UTF-8')
    all_logs = '"'.join(all_logs.split("'"))
    logs_as_json = json.loads(all_logs)
    return logs_as_json


def add_nodes(network, nodes):
    global all_saved_nodes
    for i in range(len(nodes)):
        all_saved_nodes = np.append(all_saved_nodes, nodes[i]['node_properties'])
        # Either adds local or remote node bases on config for each node
        if(nodes[i]['local']):
            # Create a local node
            network.create_node(nodes[i]['node_properties']['id'],
                                '../'+nodes[i]['eds_location'])
        else:
            # Add a remote node
            network.add_node(nodes[i]['node_properties']['id'],
                             '../'+nodes[i]['eds_location'])
    return network


def update_vehicle_status(node_id, var_name, new_value):
    ''' Send a Can message to update the vehicle status.
    '''
    global all_saved_nodes
    global network

    uncompressed_nodes = uncompress_nodes_information()
    for variable in uncompressed_nodes[node_id]['variables']:
        if(variable['node_var_name'].replace(' ', '_') == var_name):
            index = ast.literal_eval(variable['index'])
            sub_index = ast.literal_eval(variable['sub_index'])
            # do something for id
            for node in all_saved_nodes:
                if(node['name'] == variable['node_name']):
                    network[node['id']].sdo[index][sub_index].phys = new_value
                    network.sync.transmit()


def uncompress_nodes_information():
    ''' Uncompresses the shared node information.

        Return the nodes as json.
    '''
    try:
        shared_dict = shared_memory.ShareableList(name='shm_cargodash')
    except FileNotFoundError:
        return uncompress_nodes_information()
    all_nodes = zl.decompress(shared_dict[0]).decode('UTF-8')
    all_nodes = '"'.join(all_nodes.split("'"))
    nodes_as_json = json.loads(all_nodes)
    return nodes_as_json


@routes.get('/allnodes')
async def get_all_nodes(request):
    ''' Returns array with all nodes in json format.

        Eg. returns
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
        },
            ...
        ]
    '''
    return set_headers(web.json_response(uncompress_nodes_information()))


@routes.get('/node/{id}')
async def get_node(request):
    ''' Returns desired node information based on node ID.

        Parameters
            id : id of a node expects integer between 1-127 (not hex value).

        Eg. returns
        {
            type : 'DistanceNode',
            node_name : 'Front view object distance',
            variables : [
                ...
            ]
        }
    '''
    all_nodes = uncompress_nodes_information()
    try:
        node_id = int(request.match_info['id'])
    except ValueError:
        return set_headers(web.json_response(
            {'message': 'Node doesn\'t exist!'}))
    if(node_id >= 0 and node_id < len(all_nodes)):
        return set_headers(web.json_response(all_nodes[node_id]))
    else:
        return set_headers(web.json_response(
            {'message': 'Node doesn\'t exist!'}))


@routes.get('/node/{id}/{var_name}')
async def get_variable(request):
    ''' Returns desired variable in json format.

        Parameters
            id : id of a specified node expects integer between 1-127
                (not hex value).
            var_name: name of the desired variable.

        Eg. returns
        {
            name: 'variable',
            index: '0x2000',
            sub_index: '0',
            value : '900'
        }

    '''
    all_nodes = uncompress_nodes_information()
    try:
        node_id = int(request.match_info['id'])
        var_name = request.match_info['var_name']
    except ValueError:
        return set_headers(web.json_response(
            {'message': 'Variable doesn\'t exist!'}))
    if(node_id >= 0 and node_id < len(all_nodes)):
        found = False
        for variable in all_nodes[node_id]['variables']:
            if(variable['node_var_name'] == var_name):
                found = True
                return set_headers(web.json_response(variable))
        if(not found):
            return set_headers(web.json_response(
                {'message': 'Variable doesn\'t exist!'}))
    else:
        return set_headers(web.json_response(
            {'message': 'Variable doesn\'t exist!'}))


@routes.post('/node/{id}/{var_name}')
async def update_variable_value(request):
    ''' Receives a post request that wants to update a value of a variable.
        Returns a message that says value is changed succesfully.

        Parameters:
            id : id of a specified node expects integer between 1-127
                (not hex value).
            var_name: name of the variable that needs to be changed.

        Request body:
            {
                value: 'new_value'
            }

        Note: This post request has lower importance for us. Hopefully we
              are able to implement this fully.

    '''
    try:
        node_id = int(request.match_info['id'])
        var_name = request.match_info['var_name']
    except ValueError:
        return set_headers(web.json_response(
            {'message': 'Variable doesn\'t exist!'}))
    if request.body_exists:
        await_data = await request.read()
        new_data = ast.literal_eval(await_data.decode('UTF-8'))
        if(type(new_data['value']) is int):
            new_integer = int(new_data['value'])
            update_vehicle_status(node_id, var_name, new_integer)
        else:
            return set_headers(web.json_response({'message': 'Got unsupported \
            datatype value! (only support integer for now)'}))
        return set_headers(web.json_response({'message': 'Succesfully changed \
            value!'}))
    else:
        return set_headers(web.json_response({'message': 'Haven\'t received \
            a request body!'}))


@routes.get('/getloggingbuffer')
async def get_logging_buffer(request):
    ''' Returns the current logging buffer (raw messages) in as a string.

        Eg. returns
        "[
            {
                timestamp: '21314313',
                ID: '123',
                Data: 'FF 88 HA 99 12 77 88 99',
                Channel: 'vcan0'
            },
            {
                ...
            }
        ]"
    '''

    return set_headers(web.json_response(uncompress_logging_information()))

network = canopen.Network()
with open('../config.yaml', 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)
try:
    bustype = config[INTERFACE]['bustype']
    channel = config[INTERFACE]['channel']
    bitrate = config[INTERFACE]['bitrate']
    network.connect(bustype=bustype, channel=channel, bitrate=bitrate)
except OSError:
    logging.error('CanOpenListener is unable to listen to network,'
                  ' please check if configuration is set properly!'
                  f'(bustype = {bustype}, channel = {channel},'
                  f' bitrate = {bitrate})')
network = add_nodes(network, config[INTERFACE]['nodes'])

app = web.Application()
app.add_routes(routes)
web.run_app(app)
