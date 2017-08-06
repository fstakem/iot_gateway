# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.5.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from device_resource import DeviceResource
from sensor import Sensor


class Device(object):

    def __init__(self, name='', description=''):
        self.name = name
        self.description = description
        self.route = ''
        self.resource = None
        self.sensors = []

        self.create_resource()

    def create_resource(self):
        self.route = self.name.split('_')
        self.resource = DeviceResource(self.route)

    def add_sensor(self, name='', description=''):
        sensor = Sensor(name, description, self.route)
        self.sensors.append(sensor)