import datetime
import json
import math
from calcs import Calc

class Data:

    rowerId = 0

    def __init__(self, rowerId, sensor_readings, calibration_offsets):

        self.info_dict = {
            'rower_index' : rowerId,
            'seat' : self.calc_seat(rowerId),
            'datetime' : str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"))
        }

        self.data_dict = {}

        self.dict_append(sensor_readings['gyro'])
        self.dict_append(sensor_readings['scaled_gyro'])
        self.dict_append(sensor_readings['accel'])
        self.dict_append(sensor_readings['scaled_accel'])
        self.dict_append(sensor_readings['rotation'])

        self.round_data()

        # print('\nInfo dict: ', self.info_dict)
        # print('\nData dict: ', self.data_dict)

    # Processing functions

    def dict_append(self, data):
        for key, value in data.items():
            self.data_dict[key] = value

    def round_data(self):
        for key, value in self.data_dict.items():
            self.data_dict[key] = round(value, 0)

    def calc_seat(self, rower_index):
        seats = ['stroke', 'stroke2', 'bow2', 'bow']
        return seats[rower_index]

    # Get specific data functions

    def get_rower_index(self):
        return self.info_dict['rower_index']

    def get_seat_name(self):
        return self.info_dict['seat']

    def get_datetime(self):
        return self.info_dict['datetime']

    # Get dict functions

    def get_info_dict(self):
        return self.info_dict

    def get_data_dict(self):
        return self.data_dict
