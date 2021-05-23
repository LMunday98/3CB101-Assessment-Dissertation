import datetime
import json
import math
from calcs import Calc

class Data:

    rowerId = 0

    def __init__(self, rowerId, sensor_readings, calibration_offsets):
        self.sensor_readings = sensor_readings
        self.data_dict = {}
        self.info_dict = {
            'rower_index' : rowerId,
            'seat' : self.calc_seat(rowerId),
            'datetime' : str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"))
        }

        self.sensor_readings['scaled_gyro'] = self.scale_data(sensor_readings['gyro'], 131)
        self.sensor_readings['scaled_accel'] = self.scale_data(sensor_readings['accel'], 16384.0)

        self.sensor_readings['rotation'] = {
            'rx' : Calc().get_x_rotation(self.sensor_readings['scaled_accel']['sax'], self.sensor_readings['scaled_accel']['say'], self.sensor_readings['scaled_accel']['saz']),
            'ry' : Calc().get_y_rotation(self.sensor_readings['scaled_accel']['sax'], self.sensor_readings['scaled_accel']['say'], self.sensor_readings['scaled_accel']['saz'])
        }

        self.dict_append()
        self.round_data()

        # print('\nInfo dict: ', self.info_dict)
        # print('\nData dict: ', self.data_dict)

    # Processing functions

    def scale_data(self, data_array, scale):
        scaled_dict = {}
        for key, value in data_array.items():
            scaled_dict['s' + key] = value / scale
        return scaled_dict

    def dict_append(self):
        for dict_name in self.sensor_readings:
            for key, value in self.sensor_readings[dict_name].items():
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
