# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.5.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import logging

import asyncio
import aiocoap
import aiocoap.resource as resource

from device import Device
from sensor import Sensor
from sensor_resource import SensorResource
 

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

num_sensors = 5


def create_device():
    device = Device('device_1', 'Industrial Machine')

    for i in range(num_sensors):
        name = 'sensor_' + str(i+1)
        device.add_sensor(name, 'Generic Sensor')

    return device

def setup_server(device):
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

    for sensor in device.sensors:
        root.add_resource(sensor.route, sensor.resource)

    return root


def main():
    device = create_device()
    root = setup_server(device)

    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()