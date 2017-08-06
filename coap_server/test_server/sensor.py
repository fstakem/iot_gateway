# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.5.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from sensor_resource import SensorResource


class Sensor(object):

    def __init__(self, name='', description='', parent_route=''):
        self.name = name
        self.description = description
        self.route = ''
        self.resource = None

        self.create_resource(parent_route)

    def create_resource(self, parent_route):
        tokens = self.name.split('_')
        self.route = parent_route + tokens
        self.resource = SensorResource(self.route)