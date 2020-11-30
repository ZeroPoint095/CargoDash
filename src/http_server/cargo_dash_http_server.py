import asyncio
from aiohttp import web

routes = web.RouteTableDef()


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
    pass


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
    pass


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
    pass


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
              are able to implement this.

    '''
    pass


@routes.get('/getloggingbuffer')
async def get_logging_buffer(request):
    ''' Returns the current logging buffer (raw messages) in json format.

        Eg. returns
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
