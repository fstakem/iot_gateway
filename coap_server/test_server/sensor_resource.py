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

from aiocoap.resource import Resource
from aiocoap import Message


class SensorResource(Resource):

    def __init__(self, route=''):
        super(SensorResource, self).__init__()
        self.route = route
        self.rx_times = deque(maxlen=10)
        self.data = deque(maxlen=100)

    async def render_get(self, request):
        tx_rate = self.get_tx_rate()

        return Message(payload=str(tx_rate).encode("ascii"))

    async def render_put(self, request):
        self.record_time()
        current_time = datetime.now()
        self.data.append((current_time, request.payload))

        return Message()

    def record_time(self):
        current_time = datetime.now()
        self.rx_times.append(current_time)

    def get_tx_rate(self):
        q_len = len(self.rx_times)

        if q_len:
            rx_list = list(self.rx_times)
            rx_intervals = [(t - rx_list[i]) for i, t in enumerate(rx_list[1:])]

            rx_intervals = [x.total_seconds() for x in rx_intervals]

            return sum(list(rx_intervals)) / float(len(rx_intervals))

        return 0.0
