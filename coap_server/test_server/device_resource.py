# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.5.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from datetime import datetime
from collections import deque
from enum import Enum

from aiocoap.resource import Resource
from aiocoap import Message


class DeviceState(Enum):
    idle = 1
    starting = 2
    running = 3
    stopping = 4


class DeviceResource(Resource):

    def __init__(self, route=''):
        super(DeviceResource, self).__init__()
        self.route = route
        self.state = DeviceState.idle

    async def render_get(self, request):
        return Message(payload=str(self.state).encode("ascii"))

    async def render_put(self, request):
        state_strs = {x: State.__dict__[x] for x in State.__dict__ if x[0] != '_'}

        try:
            self.state = state_strs[request.payload]
        except KeyError:
            pass

        return Message(payload=str(self.state).encode("ascii"))
