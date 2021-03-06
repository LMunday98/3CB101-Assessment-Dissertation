import datetime, json, math, socket
from calcs import Calc

class Data:

    def __init__(self, rowerId, sensor_readings, calibration_offsets):
        self.sensor_readings = sensor_readings
        self.data_dict = {}
        self.info_dict = {
            'rower_index' : rowerId,
            'seat' : self.calc_seat(rowerId),
            'datetime' : str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")),
            'ip' : socket.gethostbyname(socket.gethostname())
        }

        self.sensor_readings['scaled_gyro'] = self.scale_data(sensor_readings['gyro'], 131)
        self.sensor_readings['scaled_accel'] = self.scale_data(sensor_readings['accel'], 16384.0)

        s_acc = self.sensor_readings['scaled_accel']
        raw_rx = Calc().get_x_rotation(s_acc['sax'], s_acc['say'], s_acc['saz'])
        raw_ry = Calc().get_y_rotation(s_acc['sax'], s_acc['say'], s_acc['saz'])

        self.sensor_readings['rotation'] = {
            'rx' : raw_rx - calibration_offsets['rx'],
            'ry' : raw_ry - calibration_offsets['ry']
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

    # Get dict functions

    def get_info_dict(self):
        return self.info_dict

    def get_data_dict(self):
        return self.data_dict