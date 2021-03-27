import pickle

class DataHandler:
    def __init__(self):
        self.rower_dicts = []
        self.rower_indexes = [0, 1, 2, 3]
        self.seats = ['stroke', 'stroke2', 'bow2', 'bow']
        self.measurements = ['gx', 'gy', 'gz', 'sax', 'say', 'saz', 'rx', 'ry']
        self.setup_data_dicts()

    def setup_data_dicts(self):
        for rower_index in self.rower_indexes:
            rower_dict = {}
            # Add rower id
            rower_dict['rower_index'] = rower_index
            # Add seat
            rower_dict['seat'] = self.seats[rower_index]
            # Add measurements
            for measurement in self.measurements:
                rower_dict[measurement] = 0
            self.rower_dicts.append(rower_dict)
        print(self.rower_dicts)

    def record_data(self, sent_data):
        decoded_data = pickle.loads(sent_data)
        rower_index = decoded_data.get_rowerId()
        sensor_data = decoded_data.get_sensor_data()

        print(sensor_data)