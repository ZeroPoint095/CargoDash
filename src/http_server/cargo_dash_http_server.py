import asyncio
from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/allnodes')
async def get_all_nodes(request):
    ''' Receives a get request that asks for all nodes.

        Returns array with all nodes in json format.

        Ex. returns
        [{
            type : 'DistanceNode',
            purpose : 'Front view object distance',
            variables : {
                ...
            }
        },
        {
            type : 'SteeringNode',
            purpose : 'Steering wheel',
            variables : {
                ...
            }
        },
            ...
        ]
    '''
    pass


@routes.get('/node/{id}')
async def get_node(request):
    ''' Receives a get request that asks for a specific node with a certain id.

        Parameters
            id : id of a specified node expects number.

        Returns specified node in json format.

        Ex. returns
        {
            type : 'DistanceNode',
            purpose : 'Front view object distance',
            variables : [
                ...
            ]
        }
    '''
    pass


@routes.get('/node/{id}/{var_name}')
async def get_variable(request):
    ''' Receives a get request that asks for a specific variable
        of a specified variable.

        Parameters
            id : id of a specified node expects number.
            var_name: string of a specified variable name.

        Returns specified variable in json format.

        Ex. returns
        {
            name: 'variable',
            index: '0x2000',
            sub_index: '0',
            value : '900'
        }

    '''
    pass


@routes.get('/getloggingbuffer')
async def get_logging_buffer(request):
    ''' Receives a get request that asks for the current logging buffer.

        Returns all raw can messages in json format.
        
        Ex. returns
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
    '''
    pass


app = web.Application()
app.add_routes(routes)
web.run_app(app)
