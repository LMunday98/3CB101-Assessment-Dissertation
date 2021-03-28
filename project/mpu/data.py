import datetime
import json
from .calcs import Calc

class Data:

    rowerId = 0

    def __init__(self, rowerId, gyro_readings, accel_readings, calibration_offsets, datetime):

        self.info_dict = {
            'rower_index' : rowerId,
            'seat' : self.calc_seat(rowerId),
            'datetime' : str(datetime)
        }

        self.data_dict = {}

        # Add inital gyro and accel data

        self.dict_append(gyro_readings)
        self.dict_append(accel_readings)

        # Add scaled gyro and accel data

        scaled_gyro = self.scale_data(gyro_readings, 131)
        scaled_accel = self.scale_data(accel_readings, 16384)

        self.dict_append(scaled_gyro)
        self.dict_append(scaled_accel)

        # Add rotation data

        calculations = Calc()

        self.data_dict['rx'] = calculations.get_x_rotation(scaled_accel['sax'], scaled_accel['say'], scaled_accel['saz']) - calibration_offsets[0]
        self.data_dict['ry'] = calculations.get_y_rotation(scaled_accel['sax'], scaled_accel['say'], scaled_accel['saz']) - calibration_offsets[1]

        self.round_data()

        print('\nInfo dict: ', self.info_dict)
        print('\nData dict: ', self.data_dict)

    # Processing functions

    def round_data(self):
        for key, value in self.data_dict.items():
            self.data_dict[key] = round(value, 2)

    def dict_append(self, data):
        for key, value in data.items():
            self.data_dict[key] = value

    def scale_data(self, data, scale_offset):
        scaled_dict = {}
        for key, value in data.items():
            scaled_dict['s' + key] = (value / scale_offset)
        return scaled_dict

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